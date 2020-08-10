import random
from urllib.parse import parse_qsl

from channels.generic.websocket import WebsocketConsumer
import json
import logging

from models.cluster import Cluster
from service.auth import Auth
from websocket.api.api_worker import ApiWorker
from websocket.api.exec_worker import ExecWorker
from websocket.api.log_worker import LogWorker
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
            logger.info("Receive api data: %s, %s" % (text_data, bytes_data))
            json_data = json.loads(text_data)
            self.api_worker.put_ws_action(json_data)
        except Exception as exc:
            logger.error(exc, exc_info=True)


class ExecConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.exec_worker = None

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
        params = self.scope["url_route"]["kwargs"]
        qs = self.scope.get('query_string').decode('utf-8')
        logger.info(qs)
        query = dict(parse_qsl(qs))
        logger.info(query)
        self.exec_worker = ExecWorker(self,
                                      params.get('cluster'),
                                      params.get('namespace'),
                                      params.get('pod'),
                                      container=query.get('container', ''),
                                      rows=query.get('rows', 0),
                                      cols=query.get('cols', 0))
        self.accept()
        self.exec_worker.start()

    def disconnect(self, close_code):
        if self.exec_worker:
            self.exec_worker.stop()
        logger.info("exec websocket disconnect")

    def receive(self, text_data=None, bytes_data=None):
        try:
            logger.debug("Receive exec data: %s, %s" % (text_data, bytes_data))
            # json_data = json.loads(text_data)
            self.exec_worker.put_stdin(text_data)
        except Exception as exc:
            logger.error(exc, exc_info=True)


class LogConsumer(WebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log_worker = None

    def connect(self):
        logger.info(self.scope)
        qs = self.scope.get('query_string').decode('utf-8')
        logger.info(qs)
        query = dict(parse_qsl(qs))
        logger.info(query)
        cookies = self.scope.get('cookies', {})
        if query.get('token'):
            token = query.get('token')
        else:
            token = cookies.get('osp-token')
        if not token:
            self.close("4001")
            return
        auth = Auth()
        res = auth.authenticate(token)
        if not res.is_success():
            self.close("4001")
            return
        params = self.scope["url_route"]["kwargs"]
        self.log_worker = LogWorker(self,
                                    params.get('cluster'),
                                    params.get('namespace'),
                                    params.get('pod'),
                                    query.get('container'))
        self.accept()
        self.log_worker.start()

    def disconnect(self, close_code):
        if self.log_worker:
            self.log_worker.stop()
        logger.info("log websocket disconnect")

    def receive(self, text_data=None, bytes_data=None):
        try:
            logger.debug("Receive log data: %s, %s" % (text_data, bytes_data))
            # json_data = json.loads(text_data)
        except Exception as exc:
            logger.error(exc, exc_info=True)
