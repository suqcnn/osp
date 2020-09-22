import logging
from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator, serializers
# from api.views.serializers import serviceaccount_serializers
from service.kuberesource.serviceaccount import ServiceAccountResource
from utils import CommonReturn, Code

logger = logging.getLogger(__name__)


class ServiceAccountViewSet(viewsets.GenericViewSet):

    @api_decorator('List ServiceAccounts', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        serviceaccount_resource = ServiceAccountResource(req.get("cluster"))
        query_params = {}
        if params.get('name'):
            query_params['name'] = params.get('name')
        if params.get('namespace'):
            query_params['namespace'] = params.get('namespace')
        res = serviceaccount_resource.list(query_params)
        if not res.data:
            res.data = []
        return res

    @action(methods=['GET'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)',
            url_name='get_serviceaccount')
    @api_decorator('Get ServiceAccount', serializer_class=serializers.GetResourceSerializer)
    def get(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'output': params.get('output')
        }
        serviceaccount_resource = ServiceAccountResource(req.get('cluster'))
        res = serviceaccount_resource.get(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)',
            url_name='update_ServiceAccount')
    @api_decorator('Update ServiceAccount', serializer_class=serializers.UpdateResourcesSerializer)
    def do_update_yaml(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'yaml': params.get('yaml')
        }
        serviceaccount_resource = ServiceAccountResource(req.get('cluster'))
        res = serviceaccount_resource.update(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='delete', url_name='delete_serviceaccounts')
    @api_decorator('Delete ServiceAccounts', serializer_class=serializers.DeleteResourcesSerializer)
    def delete(self, req):
        params = req.get('params')
        req_params = {
            'resources': params.get('resources')
        }
        serviceaccount_resource = ServiceAccountResource(req.get('cluster'))
        res = serviceaccount_resource.delete(req_params)
        if not res.is_success():
            return res
        return CommonReturn(Code.SUCCESS, msg="删除成功")
