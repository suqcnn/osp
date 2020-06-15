import random

from channels.generic.websocket import WebsocketConsumer
import json
import logging

from websocket.kubernetes.kubeworker import KubeWorker

logger = logging.getLogger(__name__)

p = "%s-%s" % (random.randrange(0, 100), random.randrange(0, 100))


class KubeConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kube_worker = KubeWorker(self)

    def connect(self):
        self.accept()
        self.kube_worker.start()

    def disconnect(self, close_code):
        logger.info("websocket disconnect")
        self.kube_worker.stop()
        del self.kube_worker

    def receive(self, text_data=None, bytes_data=None):
        try:
            logger.info("receive data: %s, %s" % (text_data, bytes_data))
            json_data = json.loads(text_data)
            self.kube_worker.ws_handle(json_data)
            # con = get_redis_connection("default")
            # ret_list_key = json_data.get('ret_key')
            # msg = json_data.get('msg')
            # ret_msg = '%s: %s' % (datetime.datetime.now(), msg)
            # # sleep(2)
            # rpipe = con.pipeline()
            # rpipe.lpush(ret_list_key, ret_msg).expire(ret_list_key, time=10)
            # rpipe.execute()
            # message = '运维咖啡吧：' + text_data_json['message']

            # self.send(text_data=json.dumps({
            #     'message': "from server"
            # }))
        except Exception as exc:
            logger.error(exc, exc_info=True)
