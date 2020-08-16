import logging
import uuid

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

    @action(methods=['GET'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)', url_name='get_pod')
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

    @action(methods=['POST'], detail=False, url_path='delete', url_name='delete_pod')
    @api_decorator('Delete pods', serializer_class=serializers.DeleteResourcesSerializer)
    def delete(self, req):
        params = req.get('params')
        req_params = {
            'resources': params.get('resources')
        }
        pod_resource = PodResource(req.get('cluster'))
        res = pod_resource.delete(req_params)
        if not res.is_success():
            return res
        return CommonReturn(Code.SUCCESS, msg="删除成功")

    @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)', url_name='update_pod')
    @api_decorator('Update pod', serializer_class=serializers.UpdateResourcesSerializer)
    def do_update(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'yaml': params.get('yaml')
        }
        pod_resource = PodResource(req.get('cluster'))
        res = pod_resource.update(req_params)
        return res
