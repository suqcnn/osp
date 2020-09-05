import logging
import uuid

from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator
from api.views.serializers import config_map_serializers
from service.kuberesource.config_map import ConfigMapResource
from utils import CommonReturn, Code
from . import serializers

logger = logging.getLogger(__name__)


class ConfigMapViewSet(viewsets.GenericViewSet):

    @api_decorator('List ConfigMap', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        req_params = {
            'name': params.get('name'),
            'namespace': params.get('namespace')
        }
        config_map_resource = ConfigMapResource(req.get('cluster'))
        res = config_map_resource.list(req_params)
        if not res.data:
            res.data = []
        return res

    @action(methods=['GET'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)')
    @api_decorator('Get ConfigMap', serializer_class=config_map_serializers.GetConfigMapSerializer)
    def get(self, req):
        params = req.get("params")
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'output': params.get('output')
        }
        configMap_resource = ConfigMapResource(req.get("cluster"))
        res = configMap_resource.get(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='update_config_map', url_name='update_config_map')
    @api_decorator('Update ConfigMap', serializer_class=config_map_serializers.UpdateConfigMapSerializer)
    def update_yaml(self, req):
        params = req.get('params')
        req_params = {
            'name': params.get('name'),
            'namespace': params.get('namespace'),
            'yaml': params.get('yaml')
        }
        configMapResource = ConfigMapResource(req.get('cluster'))
        res = configMapResource.update(req_params)
        return res
