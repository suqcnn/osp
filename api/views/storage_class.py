import logging
import uuid

from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator
from api.views.serializers import storage_class_serializers
from service.kuberesource.storage_class import StorageClassResource
from utils import CommonReturn, Code
from . import serializers

logger = logging.getLogger(__name__)


class StorageClassViewSet(viewsets.GenericViewSet):

    @action(methods=['GET'], detail=False, url_path='(?P<name>[^/.]+)', url_name='get_sc')
    @api_decorator('Get sc', serializer_class=storage_class_serializers.GetStorageClassSerializer)
    def get(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'output': params.get('output')
        }
        storage_class_resource = StorageClassResource(req.get('cluster'))
        res = storage_class_resource.get(req_params)
        return res

    @api_decorator('list sc', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        req_params = {
            'name': params.get('name'),
            'namespace': params.get('namespace'),
        }
        storage_class_resource = StorageClassResource(req.get('cluster'))
        res = storage_class_resource.list(req_params)
        logger.info(res.data)
        if res.is_success() and not res.data:
            res.data = []
        return res
