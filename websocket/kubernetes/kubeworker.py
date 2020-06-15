import concurrent.futures
import datetime
import json
import logging
import threading
from queue import Queue

from django_redis import get_redis_connection

from service.middlemessage import MiddleMessage

logger = logging.getLogger(__name__)


class KubeWorker(threading.Thread):

    def __init__(self, ws, *args, **kwargs):
        self.middle_request_handler = MiddleRequestHandler(ws)
        self.ws_response_handler = WSResponseHandler()
        super().__init__(*args, **kwargs)

    def run(self):
        self.middle_request_handler.start()
        self.ws_response_handler.run()
        logger.info('kube worker stoppped')

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
        super().__init__(*args, **kwargs)

    def run(self):
        while not self.has_stopped:
            try:
                for req in self.middle_message.get_request('testws'):
                    try:
                        self.ws.send(json.dumps(req))
                    except Exception as exc:
                        logger.error('send request error: %s' % exc, exc_info=True)
            except Exception as exc:
                if not self.has_stopped:
                    logger.error('get request error: %s' % exc, exc_info=True)
                    self.middle_message.close_pubsub()
        logger.info('middle request handler stopped')

    def stop(self):
        self.has_stopped = True
        self.middle_message.close_pubsub()


class WSResponseHandler:

    def __init__(self, max_worker_handlers=10):
        self.queue = Queue(maxsize=1000)
        self.has_stopped = False
        pool = concurrent.futures.ThreadPoolExecutor(int(max_worker_handlers))
        self.pool = pool

    def put_ws_response(self, data):
        self.queue.put(data)

    def put_stop(self):
        self.queue.put(0)

    def run(self):
        while not self.has_stopped:
            data = self.queue.get()
            if data != 0:
                self.pool.submit(self.ws_handle, data)
        logger.info('ws response handler stopped')

    def ws_handle(self, data):
        con = get_redis_connection("default")
        # json_data = json.loads(text_data)
        ret_list_key = data.get('ret_key')
        msg = data.get('msg')
        ret_msg = '%s: %s' % (datetime.datetime.now(), msg)
        # sleep(2)
        rpipe = con.pipeline()
        rpipe.lpush(ret_list_key, ret_msg).expire(ret_list_key, time=10)
        rpipe.execute()

    def stop(self):
        self.has_stopped = True
        self.put_stop()
