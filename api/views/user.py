import logging

from rest_framework import viewsets

from api.views import api_decorator
from utils import CommonReturn, Code
from models.user import User

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.GenericViewSet):

    @api_decorator('Create user')
    def create(self, request, params):
        u = User('tom', 'asdf', 'asdlfkje')
        u.save()
        return CommonReturn(Code.SUCCESS, 'success', u.repr())

    @api_decorator('Get user')
    def retrieve(self, request, pk):
        logger.info(pk)
        u = User.get(pk)
        res = {'name': u.name, 'email': u.email}
        return CommonReturn(Code.SUCCESS, data=res)

    @api_decorator('List user')
    def list(self, request):
        users = User.filter()
        ret = []
        for u in users:
            ret.append({
                'name': u.name,
                'email': u.email
            })
        return CommonReturn(Code.SUCCESS, data=ret)
