import logging
from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator, serializers
from api.views.serializers import daemonset_serializers
from service.kuberesource.daemonset import DaemonSetResource
from utils import CommonReturn, Code

logger = logging.getLogger(__name__)


class DaemonSetViewSet(viewsets.GenericViewSet):

    @api_decorator('List DaemonSets', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        dp_resource = DaemonSetResource(req.get("cluster"))
        query_params = {}
        if params.get('name'):
            query_params['name'] = params.get('name')
        if params.get('namespace'):
            query_params['namespace'] = params.get('namespace')
        res = dp_resource.list(query_params)
        return res

    @action(methods=['GET'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)', url_name='get_daemonset')
    @api_decorator('Get DaemonSet', serializer_class=daemonset_serializers.GetDaemonSetSerializer)
    def get(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'output': params.get('output')
        }
        dp_resource = DaemonSetResource(req.get('cluster'))
        res = dp_resource.get(req_params)
        return res

    # @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)/update_obj',
    #         url_name='update_DaemonSet_obj')
    # @api_decorator('Update DaemonSet', serializer_class=daemonset_serializers.UpdateDaemonSetObjSerializer)
    # def update_obj(self, req):
    #     params = req.get('params')
    #     req_params = {
    #         'name': req.get('name'),
    #         'namespace': req.get('namespace'),
    #         'replicas': params.get('replicas')
    #     }
    #     dp_resource = DaemonSetResource(req.get('cluster'))
    #     res = dp_resource.update_obj(req_params)
    #     return res

    @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)',
            url_name='update_DaemonSet')
    @api_decorator('Update DaemonSet', serializer_class=serializers.UpdateResourcesSerializer)
    def do_update_yaml(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'yaml': params.get('yaml')
        }
        dp_resource = DaemonSetResource(req.get('cluster'))
        res = dp_resource.update(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='delete', url_name='delete_daemonsets')
    @api_decorator('Delete DaemonSets', serializer_class=serializers.DeleteResourcesSerializer)
    def delete(self, req):
        params = req.get('params')
        req_params = {
            'resources': params.get('resources')
        }
        dp_resource = DaemonSetResource(req.get('cluster'))
        res = dp_resource.delete(req_params)
        if not res.is_success():
            return res
        return CommonReturn(Code.SUCCESS, msg="删除成功")
