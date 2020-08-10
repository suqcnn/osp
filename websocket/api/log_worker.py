import base64
import json
import logging
import threading
import uuid

from service.kuberesource.pod import PodResource
from service.middlemessage import MiddleMessage, MiddleResponse

logger = logging.getLogger(__name__)


class LogWorker(threading.Thread):

    def __init__(self, ws, cluster, namespace, pod, container='', *args, **kwargs):
        self.ws = ws
        self.cluster = cluster
        self.namespace = namespace
        self.pod = pod
        self.container = container
        self.session_id = ''
        self.has_stopped = False
        self.middle_message = MiddleMessage()
        super().__init__(*args, **kwargs)

    def run(self):
        try:
            pod_resource = PodResource(self.cluster)
            session_id = str(uuid.uuid4())
            params = {
                'namespace': self.namespace,
                'name': self.pod,
                'container': self.container,
                'session_id': session_id,
            }
            res = pod_resource.open_log(params)
            if not res.is_success():
                self.ws.send(json.dumps(res))
                self.ws.close()
                return
            self.session_id = session_id
            while not self.has_stopped:
                logger.info('start log session %s' % self.session_id)
                try:
                    for data in self.middle_message.get_logs(self.session_id):
                        if self.has_stopped:
                            break
                        try:
                            d = base64.decodebytes(data)
                            self.ws.send(d.decode('utf-8'))
                        except Exception as exc:
                            logger.error('get log error: %s' % exc, exc_info=True)
                except Exception as exc:
                    logger.error(exc)
                    if not self.stop:
                        logger.error('get log error: %s' % exc, exc_info=True)
            self.middle_message.close_log(self.session_id)
        except Exception as exc:
            logger.error("run log worker error: %s" % exc, exc_info=True)
        logger.info('log handler session %s stopped' % self.session_id)

    def stop(self):
        self.has_stopped = True
        if self.session_id:
            params = {
                'session_id': self.session_id,
            }
            pod_resource = PodResource(self.cluster)
            pod_resource.close_log(params)
            mr = MiddleResponse(self.session_id, '', MiddleResponse)
            self.middle_message.send_log(mr)
        logger.info("log worker session %s stopped success" % self.session_id)
