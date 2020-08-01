import logging

from rest_framework import viewsets

from api.views import api_decorator
from service.kuberesource.namespace import NamespaceResource
from utils import CommonReturn, Code
from . import serializers

logger = logging.getLogger(__name__)


class NamespaceViewSet(viewsets.GenericViewSet):

    @api_decorator('Create namespace')
    def create(self, req):
        return CommonReturn(Code.SUCCESS, 'success')

    @api_decorator('List namespace', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        req_params = {
            'name': params.get('name'),
        }
        ns_resource = NamespaceResource(req.get('cluster'))
        res = ns_resource.list(req_params)
        return res
