import random

from channels.generic.websocket import WebsocketConsumer
import json
import logging

from models.cluster import Cluster
from websocket.kubernetes.kubeworker import KubeWorker

logger = logging.getLogger(__name__)

p = "%s-%s" % (random.randrange(0, 100), random.randrange(0, 100))


class KubeConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.kube_worker = KubeWorker(self)

    def connect(self):
        logger.info(self.scope)
        cluster_token = ''
        for h in self.scope.get('headers'):
            if h[0] == b'token':
                cluster_token = h[1].decode('utf-8')
        if not cluster_token:
            return
        clusters = Cluster.filter(**{'token': cluster_token})
        if len(clusters) < 1:
            logger.error('Not found cluster with token %s' % cluster_token)
            return
        elif len(clusters) > 1:
            logger.error('There are more than one cluster with token %s' % cluster_token)
            return
        cluster = clusters[0]
        self.accept()
        self.kube_worker.set_cluster(cluster.name)
        self.kube_worker.start()

    def disconnect(self, close_code):
        logger.info("websocket disconnect")
        self.kube_worker.stop()
        del self.kube_worker

    def receive(self, text_data=None, bytes_data=None):
        try:
            logger.info("Receive data: %s, %s" % (text_data, bytes_data))
            json_data = json.loads(text_data)
            self.kube_worker.ws_handle(json_data)
        except Exception as exc:
            logger.error(exc, exc_info=True)
