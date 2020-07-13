import logging

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object
from . import local, REQUEST_ID_HEADER


logger = logging.getLogger(__name__)


class LocalRequestMiddleware(MiddlewareMixin):

    def process_request(self, request):
        self.set_request_id(request)
        self.set_request_ip(request)
        return

    @classmethod
    def set_request_id(cls, request):
        request_id = request.META.get(REQUEST_ID_HEADER)
        local.request_id = request_id
        request.id = local.request_id

    @classmethod
    def set_request_ip(cls, request):
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        logger.info("ip: %s, path: %s" % (ip, request.path))
        logger.info("body: %s" % (request.body,))
