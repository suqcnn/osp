import logging
import threading
from queue import Queue

from service.kuberesource.watch import WatchResource
from service.middlemessage import MiddleMessage, MiddleResponse
from utils import CommonReturn, Code

logger = logging.getLogger(__name__)


class KubeWorker(threading.Thread):

    def __init__(self, ws, *args, **kwargs):
        self.middle_request_handler = MiddleRequestHandler(ws)
        self.ws_response_handler = WSResponseHandler()
        super().__init__(*args, **kwargs)

    def set_cluster(self, cluster):
        self.middle_request_handler.set_cluster(cluster)
        self.ws_response_handler.set_cluster(cluster)

    def run(self):
        self.middle_request_handler.start()
        self.ws_response_handler.run()
        logger.info('kube worker stopped')

    def ws_handle(self, data):
        self.ws_response_handler.put_ws_response(data)

    def stop(self):
        self.middle_request_handler.stop()
        self.ws_response_handler.stop()


class MiddleRequestHandler(threading.Thread):
    def __init__(self, ws, *args, **kwargs):
        self.ws = ws
        self.middle_message = MiddleMessage()
        self.has_stopped = False
        self.cluster = None
        super().__init__(*args, **kwargs)

    def set_cluster(self, cluster):
        self.cluster = cluster

    def run(self):
        while not self.has_stopped:
            try:
                for req in self.middle_message.get_request(self.cluster):
                    try:
                        self.ws.send(req.serialize())
                    except Exception as exc:
                        logger.error('send request error: %s' % exc, exc_info=True)
                        ret = CommonReturn(code=Code.REQUEST_ERROR, msg='request error: %s' % exc)
                        response = MiddleResponse(req.request_id, ret.to_json())
                        self.middle_message.send_response(response)
            except Exception as exc:
                if not self.has_stopped:
                    logger.error('get request error: %s' % exc, exc_info=True)
                    self.middle_message.close_pubsub()
        logger.info('middle request handler stopped')

    def stop(self):
        self.has_stopped = True
        self.middle_message.close_pubsub()


class WSResponseHandler:

    def __init__(self, cluster=None,
                 # max_worker_handlers=1
                 ):
        self.queue = Queue(maxsize=1000)
        self.has_stopped = False
        self.cluster = cluster
        # pool = concurrent.futures.ThreadPoolExecutor(int(max_worker_handlers))
        # self.pool = pool
        self.middle_message = MiddleMessage()

    def put_ws_response(self, data):
        self.queue.put(data)

    def put_stop(self):
        self.queue.put(0)

    def set_cluster(self, cluster):
        self.cluster = cluster

    def run(self):
        while not self.has_stopped:
            data = self.queue.get()
            if data != 0:
                # self.pool.submit(self.ws_handle, data)
                self.ws_handle(data)
        logger.info('ws response handler stopped')

    def ws_handle(self, data):
        try:
            middle_response = MiddleResponse.unserialize(data)
            if middle_response.is_request():
                self.middle_message.send_response(middle_response)
            elif middle_response.is_watch():
                has_watch_client = self.middle_message.has_watch_client(self.cluster)
                if has_watch_client:
                    self.middle_message.send_watch(self.cluster, middle_response)
                else:
                    watch_resource = WatchResource(self.cluster)
                    watch_resource.close_watch()
            elif middle_response.is_exec():
                self.middle_message.send_stdout(middle_response)
            elif middle_response.is_log():
                self.middle_message.send_log(middle_response)
        except Exception as exc:
            logger.error('send response error: %s' % exc, exc_info=True)

    def stop(self):
        self.has_stopped = True
        self.put_stop()
