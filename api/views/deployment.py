import logging
from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator, serializers
from api.views.serializers import deployment_serializers
from service.kuberesource.deployment import DeploymentResource

logger = logging.getLogger(__name__)


class DeploymentViewSet(viewsets.GenericViewSet):

    @api_decorator('List deployment', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        dp_resource = DeploymentResource(req.get("cluster"))
        query_params = {}
        if params.get('name'):
            query_params['name'] = params.get('name')
        if params.get('namespace'):
            query_params['namespace'] = params.get('namespace')
        res = dp_resource.list(query_params)
        return res

    @action(methods=['GET'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)', url_name='get_deployment')
    @api_decorator('Get deployment', serializer_class=deployment_serializers.GetDeploymentSerializer)
    def get(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'output': params.get('output')
        }
        dp_resource = DeploymentResource(req.get('cluster'))
        res = dp_resource.get(req_params)
        return res
