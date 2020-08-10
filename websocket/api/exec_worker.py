import base64
import json
import logging
import threading
import uuid
from queue import Queue

from service.kuberesource.pod import PodResource
from service.middlemessage import MiddleMessage, MiddleResponse

logger = logging.getLogger(__name__)


class ExecWorker(threading.Thread):

    def __init__(self, ws, cluster, namespace, pod, container='', rows=0, cols=0, *args, **kwargs):
        self.queue = Queue(maxsize=1000)
        self.ws = ws
        self.cluster = cluster
        self.namespace = namespace
        self.pod = pod
        self.container = container
        self.rows = rows
        self.cols = cols
        self.has_stopped = False
        self.stdout_worker = None
        super().__init__(*args, **kwargs)

    def put_stdin(self, data):
        self.queue.put(data)

    def run(self):
        try:
            pod_resource = PodResource(self.cluster)
            session_id = str(uuid.uuid4())
            params = {
                'namespace': self.namespace,
                'name': self.pod,
                'container': self.container,
                'session_id': session_id,
                'rows': self.rows,
                'cols': self.cols
            }
            res = pod_resource.exec(params)
            if not res.is_success():
                self.ws.send(json.dumps(res))
                self.ws.close()
                return
            self.stdout_worker = StdoutWorker(self.ws, session_id)
            self.stdout_worker.start()
            while not self.has_stopped:
                data = self.queue.get()
                if data != 0:
                    params = {
                        'session_id': session_id,
                        'input': data}
                    res = pod_resource.stdin(params)
                    if not res.is_success():
                        logger.error('term stdin error: %s' % json.dumps(res.to_json()))
        except Exception as exc:
            logger.error("run exec worker error: %s" % exc, exc_info=True)
        logger.info('exec worker stopped')

    def stop(self):
        if self.stdout_worker:
            self.stdout_worker.stop()
        self.has_stopped = True
        self.put_stop()
        logger.info('exec worker stopped success')

    def put_stop(self):
        self.queue.put(0)


class StdoutWorker(threading.Thread):

    def __init__(self, ws, session_id, *args, **kwargs):
        self.ws = ws
        self.session_id = session_id
        self.has_stopped = False
        self.middle_message = MiddleMessage()
        super().__init__(*args, **kwargs)

    def run(self):
        if self.session_id:
            while not self.has_stopped:
                logger.info('start terminal stdout session %s' % self.session_id)
                try:
                    for data in self.middle_message.get_stdout(self.session_id):
                        if self.has_stopped:
                            break
                        try:
                            d = base64.decodebytes(data)
                            self.ws.send(d.decode('utf-8'))
                        except Exception as exc:
                            logger.error('get stdout error: %s' % exc, exc_info=True)
                except Exception as exc:
                    logger.error(exc)
                    if not self.stop:
                        logger.error('get stdout error: %s' % exc, exc_info=True)
            self.middle_message.close_stdout(self.session_id)
        logger.info('stdout handler session %s stopped' % self.session_id)

    def stop(self):
        self.has_stopped = True
        if self.session_id:
            mr = MiddleResponse(self.session_id, '', MiddleResponse.EXEC_TYPE)
            self.middle_message.send_stdout(mr)
        logger.info("stdout worker session %s stopped success" % self.session_id)
