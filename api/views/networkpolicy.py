import logging
from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator, serializers
from api.views.serializers import networkpolicy_serializers
from service.kuberesource.networkpolicy import NetworkPolicyResource
from utils import CommonReturn, Code

logger = logging.getLogger(__name__)


class NetworkPolicyViewSet(viewsets.GenericViewSet):

    @api_decorator('List NetworkPolicies', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        networkpolicy_resource = NetworkPolicyResource(req.get("cluster"))
        query_params = {}
        if params.get('name'):
            query_params['name'] = params.get('name')
        if params.get('namespace'):
            query_params['namespace'] = params.get('namespace')
        res = networkpolicy_resource.list(query_params)
        if not res.data:
            res.data = []
        return res

    @action(methods=['GET'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)',
            url_name='get_networkpolicy')
    @api_decorator('Get NetworkPolicy', serializer_class=networkpolicy_serializers.GetNetworkPolicySerializer)
    def get(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'output': params.get('output')
        }
        networkpolicy_resource = NetworkPolicyResource(req.get('cluster'))
        res = networkpolicy_resource.get(req_params)
        return res

    # @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)/update_obj',
    #         url_name='update_NetworkPolicy_obj')
    # @api_decorator('Update NetworkPolicy',
    # serializer_class=networkpolicy_serializers.UpdateNetworkPolicyObjSerializer)
    # def update_obj(self, req):
    #     params = req.get('params')
    #     req_params = {
    #         'name': req.get('name'),
    #         'namespace': req.get('namespace'),
    #         'replicas': params.get('replicas')
    #     }
    #     networkpolicy_resource = NetworkPolicyResource(req.get('cluster'))
    #     res = networkpolicy_resource.update_obj(req_params)
    #     return res

    @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)',
            url_name='update_NetworkPolicy')
    @api_decorator('Update NetworkPolicy', serializer_class=serializers.UpdateResourcesSerializer)
    def do_update_yaml(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'yaml': params.get('yaml')
        }
        networkpolicy_resource = NetworkPolicyResource(req.get('cluster'))
        res = networkpolicy_resource.update(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='delete', url_name='delete_networkpolicys')
    @api_decorator('Delete NetworkPolicies', serializer_class=serializers.DeleteResourcesSerializer)
    def delete(self, req):
        params = req.get('params')
        req_params = {
            'resources': params.get('resources')
        }
        networkpolicy_resource = NetworkPolicyResource(req.get('cluster'))
        res = networkpolicy_resource.delete(req_params)
        if not res.is_success():
            return res
        return CommonReturn(Code.SUCCESS, msg="删除成功")
