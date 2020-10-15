import logging
import uuid

from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator
from api.views.serializers import persistemt_volume_serializers
from service.kuberesource.persistent_volume import PersistentVolumeResource
from utils import CommonReturn, Code
from . import serializers

logger = logging.getLogger(__name__)


class PersistentVolumeViewSet(viewsets.GenericViewSet):

    @action(methods=['GET'], detail=False, url_path='(?P<name>[^/.]+)', url_name='get_pv')
    @api_decorator('Get pv', serializer_class=persistemt_volume_serializers.GetPersistentVolumeSerializer)
    def get(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'output': params.get('output')
        }
        pv_resource = PersistentVolumeResource(req.get('cluster'))
        res = pv_resource.get(req_params)
        return res

    @api_decorator('List PV', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        req_params = {
            'name': params.get('name'),
        }
        pv_resource = PersistentVolumeResource(req.get('cluster'))
        res = pv_resource.list(req_params)
        logger.info(res.data)
        if res.is_success() and not res.data:
            res.data = []
        return res

    @action(methods=['POST'], detail=False, url_path='(?P<name>[^/.]+)', url_name='update_pv')
    @api_decorator('update pv', serializer_class=serializers.UpdateResourcesSerializer)
    def do_update_yaml(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'yaml': params.get('yaml')
        }
        pv_resource = PersistentVolumeResource(req.get('cluster'))
        res = pv_resource.update(req_params)
        return res