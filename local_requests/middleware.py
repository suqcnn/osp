import logging

from django.http import JsonResponse

from service.ucenter_service import UcenterService, AuthUser

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
        r = self.set_request_user(request)
        return r

    def set_request_id(self, request):
        # 设置请求id
        request_id = request.META.get(REQUEST_ID_HEADER)
        local.request_id = request_id
        request.id = local.request_id

    def set_request_ip(self, request):
        # 设置请求IP地址
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']
        logger.info("ip: %s, path: %s" % (ip, request.path))
        logger.info("body: %s" % (request.body,))

    def set_request_user(self, request):
        # 根据token设置请求用户
        if request.path in ('/health', '/health/', 'health'):
            return
        token = request.GET.get('token')
        if not token:
            token = request.META.get('HTTP_ACCESS_TOKEN')
        if not token:
            token = request.COOKIES.get('Access-Token')
        local.request_token = token
        logger.info('token: %s' % token)
        if not token:
            return JsonResponse({'sso_url': UcenterService.SSO_LOGIN_URL}, status=401)
        res = UcenterService.auth_token(token)
        if not res.is_success():
            return JsonResponse({'sso_url': UcenterService.SSO_LOGIN_URL}, status=401)
        user_info = res.data.get('user')
        user = AuthUser(user_info.get('acct_user_id'), user_info.get('customerId'), user_info.get('username'))
        # user = AuthUser('577303', 'E888996')
        request.auth_user = user
