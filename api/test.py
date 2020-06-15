import datetime
import json
import logging
import random
from time import sleep

from django.http import HttpResponse
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)


def health(req):
    logger.info(t.global_data)
    r = random.randrange(0, 10)
    logger.info(r)
    t.update_data(r)
    return HttpResponse('ok')


class Test:

    def __init__(self):
        self.global_data = []

    def update_data(self, value):
        self.global_data.append(value)


t = Test()

p = "%s-%s" % (random.randrange(0, 100), random.randrange(0, 100))


def ws_mock(req):
    try:
        con = get_redis_connection("default")
        cp = con.connection_pool

        ws_sub = con.pubsub()
        ws_sub.subscribe('testws')
        ws_sub.get_message()
        for data in ws_sub.listen():
            logger.info("%s- created connections: %s" % (p, cp._created_connections))
            # data = ws_sub.get_message()['data']
            d = data.get('data')
            logger.info('%s- receive data: %s' % (p, data))
            try:
                json_data = json.loads(d)
            except Exception as exc:
                logger.error(exc, exc_info=True)
                continue
            ret_list_key = json_data.get('ret_key')
            msg = json_data.get('msg')
            ret_msg = '%s: %s' % (datetime.datetime.now(), msg)
            sleep(2)
            con.lpush(ret_list_key, ret_msg)
    except Exception as exc:
        logger.error(exc, exc_info=True)
    return HttpResponse('finish')


def test_con(req):
    con = get_redis_connection("default")
    cp = con.connection_pool
    logger.info("%s- before created connections: %s" % (p, cp._created_connections))
    r = random.randrange(0, 100)
    logger.info("%s- random: %s" % (p, r))
    ret_key = '%s:%s' % (p, r)
    pub_data = {'ret_key': ret_key, 'msg': r}
    subnums = con.pubsub_numsub('testws')
    logger.info(subnums)
    has_sub = False
    for s in subnums:
        logger.info(s)
        logger.info(type(s[0].decode('utf-8')))
        if s[0].decode('utf-8') == 'testws' and s[1] > 0:
            has_sub = True
            break
    if has_sub:
        con.publish('testws', json.dumps(pub_data))
        d = con.blpop(ret_key)
        logger.info(d)
        con.delete(ret_key)
        return HttpResponse(d)
    return HttpResponse('not sub')
