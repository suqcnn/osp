import logging
import uuid

from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator
from api.views.serializers import secret_serializers
from service.kuberesource.hpa import HpaResource
from utils import CommonReturn, Code
from . import serializers

logger = logging.getLogger(__name__)
# HorizontalPodAutoscalers

class HorizontalPodAutoscalersViewSet(viewsets.GenericViewSet):

    @api_decorator('List HorizontalPodAutoscalers', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        req_params = {
            'name': params.get('name'),
            'namespace': params.get('namespace')
        }
        hpa_resource = HpaResource(req.get('cluster'))
        res = hpa_resource.list(req_params)
        if not res.data:
            res.data = []
        return res

    @action(methods=['GET'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)')
    @api_decorator('Get HorizontalPodAutoscalers', serializer_class=secret_serializers.GetSecretSerializer)
    def get(self, req):
        params = req.get("params")
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'output': params.get('output')
        }
        hpa_resource = HpaResource(req.get("cluster"))
        res = hpa_resource.get(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)',
            url_name='update_hpa')
    @api_decorator('Update hpa', serializer_class=serializers.UpdateResourcesSerializer)
    def update_yaml(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'yaml': params.get('yaml')
        }
        dp_resource = HpaResource(req.get('cluster'))
        res = dp_resource.update(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='update_hpa', url_name='update_hpa')
    @api_decorator('Update Secret', serializer_class=secret_serializers.UpdateSecretSerializer)
    def update_hpa(self, req):
        params = req.get('params')
        req_params = {
            'name': params.get('name'),
            'namespace': params.get('namespace'),
            'yaml': params.get('yaml')
        }
        hpa_resource = HpaResource(req.get('cluster'))
        res = hpa_resource.update(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='delete', url_name='delete_hpa')
    @api_decorator('Delete hpa', serializer_class=serializers.DeleteResourcesSerializer)
    def delete(self, req):
        params = req.get('params')
        req_params = {
            'resources': params.get('resources')
        }
        hpa_resource = HpaResource(req.get('cluster'))
        res = hpa_resource.delete(req_params)
        if not res.is_success():
            return res
        return CommonReturn(Code.SUCCESS, msg="删除成功")