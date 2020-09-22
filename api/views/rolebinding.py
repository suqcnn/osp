import logging
from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator, serializers
# from api.views.serializers import rolebinding_serializers
from service.kuberesource.rolebinding import RoleBindingResource
from utils import CommonReturn, Code

logger = logging.getLogger(__name__)


class RoleBindingViewSet(viewsets.GenericViewSet):

    @api_decorator('List RoleBindings', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        rolebinding_resource = RoleBindingResource(req.get("cluster"))
        query_params = {}
        if params.get('name'):
            query_params['name'] = params.get('name')
        if params.get('namespace'):
            query_params['namespace'] = params.get('namespace')
        res = rolebinding_resource.list(query_params)
        if not res.data:
            res.data = []
        return res

    @action(methods=['GET'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)',
            url_name='get_rolebinding')
    @api_decorator('Get RoleBinding', serializer_class=serializers.GetResourceSerializer)
    def get(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'output': params.get('output'),
            'kind': params.get('kind'),
        }
        rolebinding_resource = RoleBindingResource(req.get('cluster'))
        res = rolebinding_resource.get(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)',
            url_name='update_RoleBinding')
    @api_decorator('Update RoleBinding', serializer_class=serializers.UpdateResourcesSerializer)
    def do_update_yaml(self, req):
        params = req.get('params')
        namespace = req.get('namespace')
        if params.get('kind') == 'ClusterRoleBinding':
            namespace = ''
        req_params = {
            'name': req.get('name'),
            'namespace': namespace,
            'yaml': params.get('yaml'),
            'kind': params.get('kind')
        }
        rolebinding_resource = RoleBindingResource(req.get('cluster'))
        res = rolebinding_resource.update(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='delete', url_name='delete_rolebindings')
    @api_decorator('Delete RoleBindings', serializer_class=serializers.DeleteResourcesSerializer)
    def delete(self, req):
        params = req.get('params')
        req_params = {
            'resources': params.get('resources')
        }
        rolebinding_resource = RoleBindingResource(req.get('cluster'))
        res = rolebinding_resource.delete(req_params)
        if not res.is_success():
            return res
        return CommonReturn(Code.SUCCESS, msg="删除成功")
