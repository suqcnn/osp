import logging
import uuid

from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator
from api.views.serializers import secret_serializers
from service.kuberesource.secret import SecretResource
from utils import CommonReturn, Code
from . import serializers

logger = logging.getLogger(__name__)


class SecretViewSet(viewsets.GenericViewSet):

    @api_decorator('List Secret', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        req_params = {
            'name': params.get('name'),
            'namespace': params.get('namespace')
        }
        secret_resource = SecretResource(req.get('cluster'))
        res = secret_resource.list(req_params)
        if not res.data:
            res.data = []
        return res

    @action(methods=['GET'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)')
    @api_decorator('Get Secret', serializer_class=secret_serializers.GetSecretSerializer)
    def get(self, req):
        params = req.get("params")
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'output': params.get('output')
        }
        secret_resource = SecretResource(req.get("cluster"))
        res = secret_resource.get(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='update_secret', url_name='update_config_map')
    @api_decorator('Update Secret', serializer_class=secret_serializers.UpdateSecretSerializer)
    def update_yaml(self, req):
        params = req.get('params')
        req_params = {
            'name': params.get('name'),
            'namespace': params.get('namespace'),
            'yaml': params.get('yaml')
        }
        secret_resource = SecretResource(req.get('cluster'))
        res = secret_resource.update(req_params)
        return res
