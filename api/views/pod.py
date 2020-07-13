import logging

from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator
from api.views.serializers import pod_serializers
from service.kuberesource.pod import PodResource
from utils import CommonReturn, Code
from . import serializers

logger = logging.getLogger(__name__)


class PodViewSet(viewsets.GenericViewSet):

    @api_decorator('Create pod')
    def create(self, req):
        return CommonReturn(Code.SUCCESS, 'success')

    @action(methods=['GET'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)')
    @api_decorator('Get pod', serializer_class=pod_serializers.GetPodSerializer)
    def get(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'output': params.get('output')
        }
        pod_resource = PodResource(req.get('cluster'))
        res = pod_resource.get(req_params)
        return res

    @api_decorator('List pods', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        req_params = {
            'name': params.get('name'),
            'namespace': params.get('namespace')
        }
        pod_resource = PodResource(req.get('cluster'))
        res = pod_resource.list(req_params)
        return res
