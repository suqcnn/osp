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

    @action(['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)/exec')
    @api_decorator('Exec pods', serializer_class=pod_serializers.ExecPodSerializer)
    def exec(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'container': params.get('container'),
            'session_id': str(uuid.uuid4())
        }
        pod_resource = PodResource(req.get('cluster'))
        res = pod_resource.exec(req_params)
        if not res.is_success():
            return res
        return CommonReturn(Code.SUCCESS, data={'session_id': req_params.get('session_id')})

    @action(['POST'], detail=False, url_path='stdin')
    @api_decorator('Stdin container', serializer_class=pod_serializers.PodStdinSerializer)
    def stdin(self, req):
        params = req.get('params')
        req_params = {
            'session_id': params.get('session_id'),
            'input': params.get('input')
        }
        pod_resource = PodResource(req.get('cluster'))
        res = pod_resource.stdin(req_params)
        return res
