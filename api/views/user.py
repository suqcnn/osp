import json
import logging

from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator
from api.views.serializers import user_serializers
from service.auth import Auth
from utils import CommonReturn, Code, tools, CommonException
from models.user import User

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.GenericViewSet):

    @api_decorator('Create user', serializer_class=user_serializers.CreateUserSerializer)
    def create(self, req):
        params = req.get('params')
        encrypted_pwd = tools.encrypt(params.get('password'))
        u = User(name=params.get('name'),
                 email=params.get('email'),
                 password=encrypted_pwd)
        u.save()
        res = {
            'name': u.name,
            'email': u.email
        }
        return CommonReturn(Code.SUCCESS, 'Success', res)

    @action(methods=['POST'], detail=False, url_path='admin')
    @api_decorator('Create admin', serializer_class=user_serializers.CreateAdminSerializer, login_required=False)
    def admin(self, req):
        username = 'admin'
        try:
            User.get(username)
        except CommonException as exc:
            if exc.code == Code.DATA_NOT_EXISTS:
                params = req.get('params')
                encrypted_pwd = tools.encrypt(params.get('password'))
                u = User(name=username,
                         email=params.get('email', ''),
                         password=encrypted_pwd)
                u.save()
                res = {
                    'name': u.name,
                    'email': u.email
                }
                return CommonReturn(Code.SUCCESS, 'Success', res)
            else:
                return CommonReturn(exc.code, exc.msg)
        except Exception as exc:
            logger.error('get admin user error: %s' % exc, exc_info=True)
            return CommonReturn(Code.UNKNOWN_ERROR, str(exc))
        return CommonReturn(Code.DATA_EXISTS, 'Admin user has exists')

    @api_decorator('Get user')
    def retrieve(self, req):
        pk = req.get('pk')
        u = User.get(pk)
        res = {'name': u.name, 'email': u.email}
        return CommonReturn(Code.SUCCESS, data=res)

    @api_decorator('List user')
    def list(self, req):
        users = User.filter()
        params = req.get('params', {})
        ret = []
        name = params.get('name')
        for u in users:
            if not name or u.name.contains(name):
                ret.append({
                    'name': u.name,
                    'email': u.email
                })
        return CommonReturn(Code.SUCCESS, data=ret)


def login(req):
    try:
        body = json.loads(req.body)
        username = body.get('username')
        password = body.get('password')
        if not username:
            return JsonResponse({'code': Code.PARAM_ERROR, 'msg': 'Parameter username is blank'})
        if not password:
            return JsonResponse({'code': Code.PARAM_ERROR, 'msg': 'Parameter password is blank'})
        res = Auth.login(username, password)
        if not res.is_success():
            return JsonResponse(res.to_json(), status=401)
        return JsonResponse(res.to_json())
    except Exception as exc:
        logger.error('login error: %s' % exc, exc_info=True)
        return JsonResponse({'code': Code.AUTH_ERROR, 'msg': str(exc)})
