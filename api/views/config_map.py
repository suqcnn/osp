import logging
import uuid

from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator
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
        return res
