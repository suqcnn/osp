import random

from channels.generic.websocket import WebsocketConsumer
import json
import logging

from models.cluster import Cluster
from service.auth import Auth
from websocket.api.worker import ApiWorker
from websocket.kubernetes.kubeworker import KubeWorker

logger = logging.getLogger(__name__)

p = "%s-%s" % (random.randrange(0, 100), random.randrange(0, 100))


class ApiConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api_worker = ApiWorker(self)

    def connect(self):
        logger.info(self.scope)
        cookies = self.scope.get('cookies', {})
        token = cookies.get('osp-token')
        if not token:
            self.close("4001")
            return
        auth = Auth()
        res = auth.authenticate(token)
        if not res.is_success():
            self.close("4001")
            return
        self.accept()
        self.api_worker.start()

    def disconnect(self, close_code):
        self.api_worker.stop()
        logger.info("api websocket disconnect")

    def receive(self, text_data=None, bytes_data=None):
        try:
            logger.info("Receive data: %s, %s" % (text_data, bytes_data))
            json_data = json.loads(text_data)
            self.api_worker.put_ws_action(json_data)
        except Exception as exc:
            logger.error(exc, exc_info=True)
