import json
import logging
import uuid

from django_redis import get_redis_connection

from utils import CommonException, Code

logger = logging.getLogger(__name__)


class MiddleMessage:

    def __init__(self):
        self.connection = get_redis_connection()

    @property
    def pubsub(self):
        if not hasattr(self, '_pubsub'):
            setattr(self, '_pubsub', self.connection.pubsub())
        return getattr(self, '_pubsub')

    def close_pubsub(self):
        if hasattr(self, '_pubsub'):
            try:
                p = getattr(self, '_pubsub')
                p.close()
                delattr(self, '_pubsub')
            except Exception as exc:
                logger.error('Close pubsub error: %s' % exc, exc_info=True)

    @classmethod
    def cluster_request_queue_key(cls, cluster):
        return 'osp:cluster_request:%s' % cluster

    def get_request(self, cluster):
        request_queue_key = self.cluster_request_queue_key(cluster)
        self.pubsub.subscribe(request_queue_key)
        for data in self.pubsub.listen():
            try:
                logger.debug('receive data: %s' % data)
                d = data.get('data')
                if d == 1:
                    continue
                try:
                    data = json.loads(d)
                except Exception as exc:
                    logger.error('subscribe data json error: %s' % exc, exc_info=True)
                    continue
                middle_request = MiddleRequest.unserialize(data)
                yield middle_request
            except Exception as exc:
                logger.error('websocket handle subscribe data error: %s' % exc, exc_info=True)

    @classmethod
    def cluster_watch_queue_key(cls, cluster):
        return 'osp:cluster_watch:%s' % cluster

    def get_watch(self, cluster):
        watch_queue_key = self.cluster_watch_queue_key(cluster)
        self.pubsub.subscribe(watch_queue_key)
        for data in self.pubsub.listen():
            try:
                logger.info('receive watch data: %s' % data)
                d = data.get('data')
                if d == 1:
                    continue
                try:
                    data = json.loads(d)
                except Exception as exc:
                    logger.error('subscribe data json error: %s' % exc, exc_info=True)
                    continue
                # watch_response = MiddleResponse.unserialize(data)
                yield data
            except Exception as exc:
                logger.error('websocket handle subscribe data error: %s' % exc, exc_info=True)

    def send_response(self, middle_response):
        request_id = middle_response.request_id
        response_data = middle_response.serialize_data()
        pipeline = self.connection.pipeline()
        pipeline.lpush(request_id, response_data).expire(request_id, time=10)
        pipeline.execute()

    def has_watch_client(self, cluster):
        watch_queue_key = self.cluster_watch_queue_key(cluster)
        subscribes = self.connection.pubsub_numsub(watch_queue_key)
        logger.info('token %s current subscribes: %s' % (watch_queue_key, subscribes))
        for s in subscribes:
            if s[0].decode('utf-8') == watch_queue_key and s[1] > 0:
                return True
        return False

    def send_watch(self, cluster, middle_response):
        watch_queue_key = self.cluster_watch_queue_key(cluster)
        subscribes = self.connection.pubsub_numsub(watch_queue_key)
        logger.info('token %s current subscribes: %s' % (watch_queue_key, subscribes))
        has_sub = False
        for s in subscribes:
            if s[0].decode('utf-8') == watch_queue_key and s[1] > 0:
                has_sub = True
                break
        if has_sub:
            self.connection.publish(watch_queue_key, middle_response.serialize_data())

    def send_request(self, middle_request):
        request_queue_key = self.cluster_request_queue_key(middle_request.cluster)
        subscribes = self.connection.pubsub_numsub(request_queue_key)
        logger.debug('token %s current subscribes: %s' % (request_queue_key, subscribes))
        has_sub = False
        for s in subscribes:
            if s[0].decode('utf-8') == request_queue_key and s[1] > 0:
                has_sub = True
                break
        if has_sub:
            self.connection.publish(request_queue_key, middle_request.serialize())
            response_data = self.connection.blpop(middle_request.request_id, timeout=middle_request.timeout)
            if response_data is None:
                raise CommonException(Code.REQUEST_ERROR, 'request kubernetes agent timeout')
            self.connection.delete(middle_request.request_id)
            return response_data[1]
        raise CommonException(Code.REQUEST_ERROR, 'connect kubernetes agent error')

    @classmethod
    def term_stdout_queue_key(cls, session_id):
        return 'osp:term_stdout:%s' % session_id

    def get_stdout(self, session_id):
        logger.info('get stdout from session id: %s' % session_id)
        session_key = self.term_stdout_queue_key(session_id)
        while True:
            response_data = self.connection.brpop(session_key)
            if response_data is None:
                raise CommonException(Code.REQUEST_ERROR, 'get exec stdout error')
            yield response_data[1]

    def send_stdout(self, middle_response):
        request_id = middle_response.request_id
        session_key = self.term_stdout_queue_key(request_id)
        pipeline = self.connection.pipeline()
        pipeline.lpush(session_key, middle_response.data)
        pipeline.execute()

    def close_stdout(self, session_id):
        session_key = self.term_stdout_queue_key(session_id)
        self.connection.expire(session_key, 3)
        self.connection.delete(session_key)

    @classmethod
    def log_queue_key(cls, session_id):
        return 'osp:log:%s' % session_id

    def get_logs(self, session_id):
        logger.info('get logs from session id: %s' % session_id)
        session_key = self.log_queue_key(session_id)
        while True:
            response_data = self.connection.brpop(session_key)
            if response_data is None:
                raise CommonException(Code.REQUEST_ERROR, 'get logs error')
            yield response_data[1]

    def send_log(self, middle_response):
        request_id = middle_response.request_id
        session_key = self.log_queue_key(request_id)
        pipeline = self.connection.pipeline()
        pipeline.lpush(session_key, middle_response.data)
        pipeline.execute()

    def close_log(self, session_id):
        session_key = self.log_queue_key(session_id)
        self.connection.expire(session_key, 3)
        self.connection.delete(session_key)


class MiddleRequest:

    def __init__(self, cluster=None, request_id=None, resource=None, action=None, params=None, timeout=30):
        self.cluster = cluster
        self._request_id = request_id
        self.resource = resource
        self.action = action
        self.params = params
        self.timeout = timeout

    @property
    def request_id(self):
        if not self._request_id:
            self._request_id = str(uuid.uuid4().hex)
        return self._request_id

    def serialize(self):
        return json.dumps({
            'cluster': self.cluster,
            'request_id': self.request_id,
            'resource': self.resource,
            'action': self.action,
            'params': self.params
        })

    @classmethod
    def unserialize(cls, data):
        return cls(cluster=data.get('cluster'),
                   request_id=data.get('request_id'),
                   resource=data.get('resource'),
                   action=data.get('action'),
                   params=data.get('params'))


class MiddleResponse:
    REQUEST_TYPE = 'request'
    WATCH_TYPE = 'watch'
    EXEC_TYPE = 'exec'
    LOG_TYPE = 'log'

    def __init__(self, request_id=None, data=None, res_type=None):
        self.request_id = request_id
        self.res_type = res_type
        self.data = data

    def serialize_data(self):
        return json.dumps(self.data)

    @classmethod
    def unserialize(cls, data):
        return cls(request_id=data.get('request_id'),
                   res_type=data.get('res_type'),
                   data=data.get('data'))

    def is_request(self):
        return self.res_type == self.REQUEST_TYPE

    def is_watch(self):
        return self.res_type == self.WATCH_TYPE

    def is_exec(self):
        return self.res_type == self.EXEC_TYPE

    def is_log(self):
        return self.res_type == self.LOG_TYPE
