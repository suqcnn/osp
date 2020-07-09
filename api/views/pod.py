import logging

from rest_framework import viewsets

from api.views import api_decorator
from service.kuberesource.pod import PodResource
from utils import CommonReturn, Code
from . import serializers

logger = logging.getLogger(__name__)


class PodViewSet(viewsets.GenericViewSet):

    @api_decorator('Create pod')
    def create(self, req):
        return CommonReturn(Code.SUCCESS, 'success')

    @api_decorator('Get pod')
    def retrieve(self, req):
        pk = req.get('pk')
        cluster = req.get('cluster')
        logger.info(pk)
        logger.info(cluster)
        return CommonReturn(Code.SUCCESS)

    @api_decorator('List pods', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        pod_resource = PodResource(req.get('cluster'))
        params = req.get('params')
        req_params = {
            'name': params.get('name'),
            'namespace': params.get('namespace')
        }
        res = pod_resource.list(req_params)
        return res
