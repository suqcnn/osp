import datetime
import logging

from django_redis import get_redis_connection

from utils import CommonException, Code

logger = logging.getLogger(__name__)


class Model:

    PREFIX = 'osp'

    def __init__(self, pk=None):
        self.conn = get_redis_connection()
        self.pk = pk

    @property
    def primary_key(self):
        return self.pk

    @classmethod
    def class_name(cls):
        return cls.__name__.lower()

    @classmethod
    def latest_primary_id_key(cls):
        return '%s:%s:latest_id' % (cls.PREFIX, cls.class_name())

    def increment_latest_primary_id(self):
        return self.conn.incr(self.latest_primary_id_key())

    @classmethod
    def set_key(cls):
        return '%s:%s:_sets' % (cls.PREFIX, cls.class_name())

    @classmethod
    def cache_key(cls, primary_id):
        return '%s:%s:%s' % (cls.PREFIX, cls.class_name(), str(primary_id))

    def add_to_set(self, primary_id):
        return self.conn.sadd(self.set_key(), str(primary_id))

    def repr(self):
        raise CommonException(Code.NOT_IMPLEMENTATION, '%s class has no repr method' % self.__class__.__name__)

    @classmethod
    def unrepr(cls, **kwargs):
        return cls(**kwargs)

    def save(self):
        primary_id = self.primary_key
        if not primary_id:
            primary_id = self.increment_latest_primary_id()
        added = self.add_to_set(primary_id)
        if not added:
            raise CommonException(Code.DATA_DUPLICATION, 'primary key duplicated')
        r = self.repr()
        if not r.get('create_time'):
            r['create_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        if not r.get('update_time'):
            r['update_time'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        res = self.conn.hmset(self.cache_key(primary_id), r)
        logger.info(res)
        return self

    @classmethod
    def get(cls, pk):
        conn = get_redis_connection()
        primary_key = cls.cache_key(pk)
        logger.info(primary_key)
        res = conn.hgetall(primary_key)
        logger.info(res)
        if not res:
            raise CommonException(Code.DATA_NOT_EXISTS, 'Not found %s %s' % (str(pk), cls.class_name()))
        data = {}
        for k, v in res.items():
            data[k.decode('utf-8')] = v.decode('utf-8')
        return cls.unrepr(**data)

    @classmethod
    def filter(cls, **kwargs):
        conn = get_redis_connection()
        instances = []
        for pk in conn.smembers(cls.set_key()):
            pk = pk.decode('utf-8')
            instance = cls.get(pk)
            if kwargs:
                for k, v in kwargs.items():
                    if hasattr(instance, k) and getattr(instance, k) == v:
                        instances.append(instance)
            else:
                instances.append(instance)
        return instances
