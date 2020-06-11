import logging

from . import local


class RequestIDFilter(logging.Filter):

    def filter(self, record):
        record.request_id = local.request_id
        return True
