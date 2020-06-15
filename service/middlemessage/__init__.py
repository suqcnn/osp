import json
import logging

from django_redis import get_redis_connection

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
            p = getattr(self, '_pubsub')
            p.close()
            delattr(self, '_pubsub')

    def get_request(self, token):
        self.pubsub.subscribe(token)
        for data in self.pubsub.listen():
            try:
                logger.info('receive data: %s' % data)
                d = data.get('data')
                if d == 1:
                    continue
                try:
                    data = json.loads(d)
                except Exception as exc:
                    logger.error('subscribe data json error: %s' % exc, exc_info=True)
                    continue
                yield data
            except Exception as exc:
                logger.error('websocket handle subscribe data error: %s' % exc, exc_info=True)
