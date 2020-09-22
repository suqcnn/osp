import logging
from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator, serializers
# from api.views.serializers import role_serializers
from service.kuberesource.role import RoleResource
from utils import CommonReturn, Code

logger = logging.getLogger(__name__)


class RoleViewSet(viewsets.GenericViewSet):

    @api_decorator('List Roles', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        role_resource = RoleResource(req.get("cluster"))
        query_params = {}
        if params.get('name'):
            query_params['name'] = params.get('name')
        if params.get('namespace'):
            query_params['namespace'] = params.get('namespace')
        res = role_resource.list(query_params)
        if not res.data:
            res.data = []
        return res

    @action(methods=['GET'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)',
            url_name='get_role')
    @api_decorator('Get Role', serializer_class=serializers.GetResourceSerializer)
    def get(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'output': params.get('output'),
            'kind': params.get('kind')
        }
        role_resource = RoleResource(req.get('cluster'))
        res = role_resource.get(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)',
            url_name='update_Role')
    @api_decorator('Update Role', serializer_class=serializers.UpdateResourcesSerializer)
    def do_update_yaml(self, req):
        params = req.get('params')
        namespace = req.get('namespace')
        if params.get('kind') == 'ClusterRole':
            namespace = ''
        req_params = {
            'name': req.get('name'),
            'namespace': namespace,
            'yaml': params.get('yaml'),
            'kind': params.get('kind')
        }
        role_resource = RoleResource(req.get('cluster'))
        res = role_resource.update(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='delete', url_name='delete_roles')
    @api_decorator('Delete Roles', serializer_class=serializers.DeleteResourcesSerializer)
    def delete(self, req):
        params = req.get('params')
        req_params = {
            'resources': params.get('resources')
        }
        role_resource = RoleResource(req.get('cluster'))
        res = role_resource.delete(req_params)
        if not res.is_success():
            return res
        return CommonReturn(Code.SUCCESS, msg="删除成功")
