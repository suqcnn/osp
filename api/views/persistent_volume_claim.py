import logging
import uuid

from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator
from api.views.serializers import persistemt_volume_claim_serializers
from service.kuberesource.persistent_volume_claim import PersistentVolumeClaimResource
from utils import CommonReturn, Code
from . import serializers

logger = logging.getLogger(__name__)


class PersistentVolumeClaimViewSet(viewsets.GenericViewSet):

    @action(methods=['GET'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)', url_name='get_pvc')
    @api_decorator('get pvc', serializer_class=persistemt_volume_claim_serializers.GetPersistentVolumeClaimSerializer)
    def get(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'output': params.get('output')
        }
        pvc_resource = PersistentVolumeClaimResource(req.get('cluster'))
        res = pvc_resource.get(req_params)
        return res

    @api_decorator('list pvc', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        req_params = {
            'name': params.get('name'),
            'namespace': params.get('namespace'),
        }
        pvc_resource = PersistentVolumeClaimResource(req.get('cluster'))
        res = pvc_resource.list(req_params)
        logger.info(res.data)
        if res.is_success() and not res.data:
            res.data = []
        return res
