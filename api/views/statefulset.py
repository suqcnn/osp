import logging
from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator, serializers
from api.views.serializers import statefulset_serializers
from service.kuberesource.statefulset import StatefulSetResource
from utils import CommonReturn, Code

logger = logging.getLogger(__name__)


class StatefulSetViewSet(viewsets.GenericViewSet):

    @api_decorator('List StatefulSets', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        dp_resource = StatefulSetResource(req.get("cluster"))
        query_params = {}
        if params.get('name'):
            query_params['name'] = params.get('name')
        if params.get('namespace'):
            query_params['namespace'] = params.get('namespace')
        res = dp_resource.list(query_params)
        return res

    @action(methods=['GET'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)', url_name='get_statefulset')
    @api_decorator('Get StatefulSet', serializer_class=statefulset_serializers.GetStatefulsetSerializer)
    def get(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'output': params.get('output')
        }
        dp_resource = StatefulSetResource(req.get('cluster'))
        res = dp_resource.get(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)/update_obj',
            url_name='update_statefulset_obj')
    @api_decorator('Update StatefulSet', serializer_class=statefulset_serializers.UpdateStatefulsetObjSerializer)
    def update_obj(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'replicas': params.get('replicas')
        }
        dp_resource = StatefulSetResource(req.get('cluster'))
        res = dp_resource.update_obj(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)',
            url_name='update_statefulset')
    @api_decorator('Update StatefulSet', serializer_class=serializers.UpdateResourcesSerializer)
    def do_update_yaml(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'yaml': params.get('yaml')
        }
        dp_resource = StatefulSetResource(req.get('cluster'))
        res = dp_resource.update(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='delete', url_name='delete_statefulsets')
    @api_decorator('Delete StatefulSets', serializer_class=serializers.DeleteResourcesSerializer)
    def delete(self, req):
        params = req.get('params')
        req_params = {
            'resources': params.get('resources')
        }
        dp_resource = StatefulSetResource(req.get('cluster'))
        res = dp_resource.delete(req_params)
        if not res.is_success():
            return res
        return CommonReturn(Code.SUCCESS, msg="删除成功")
