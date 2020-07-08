import logging

from rest_framework import viewsets

from api.views import api_decorator
from service.kuberesource.pod import PodResource
from utils import CommonReturn, Code
from . import serializers
from .serializers import pod_serializers

logger = logging.getLogger(__name__)


class PodViewSet(viewsets.GenericViewSet):

    @api_decorator('Create pod')
    def create(self, request, params):
        return CommonReturn(Code.SUCCESS, 'success')

    @api_decorator('Get pod')
    def retrieve(self, request, pk):
        return CommonReturn(Code.SUCCESS)

    @api_decorator('List pod', serializer_class=pod_serializers.ListPodSerializer)
    def list(self, request, params):
        pod_resource = PodResource(params.get('cluster'))
        req_params = {
            'name': params.get('name'),
            'namespace': params.get('namespace')
        }
        res = pod_resource.list(req_params)
        return res
