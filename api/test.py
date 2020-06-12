import logging
import random

from django.http import HttpResponse


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
