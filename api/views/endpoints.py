import logging
from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator, serializers
from api.views.serializers import endpoints_serializers
from service.kuberesource.endpoints import EndpointsResource
from utils import CommonReturn, Code

logger = logging.getLogger(__name__)


class EndpointsViewSet(viewsets.GenericViewSet):

    @api_decorator('List endpoints', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        endpoints_resource = EndpointsResource(req.get("cluster"))
        query_params = {}
        if params.get('name'):
            query_params['name'] = params.get('name')
        if params.get('namespace'):
            query_params['namespace'] = params.get('namespace')
        res = endpoints_resource.list(query_params)
        if not res.data:
            res.data = []
        return res

    @action(methods=['GET'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)', url_name='get_endpoints')
    @api_decorator('Get Endpoints', serializer_class=endpoints_serializers.GetEndpointsSerializer)
    def get(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'output': params.get('output')
        }
        endpoints_resource = EndpointsResource(req.get('cluster'))
        res = endpoints_resource.get(req_params)
        return res

    # @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)/update_obj',
    #         url_name='update_Endpoints_obj')
    # @api_decorator('Update Endpoints', serializer_class=endpoints_serializers.UpdateEndpointsObjSerializer)
    # def update_obj(self, req):
    #     params = req.get('params')
    #     req_params = {
    #         'name': req.get('name'),
    #         'namespace': req.get('namespace'),
    #         'replicas': params.get('replicas')
    #     }
    #     endpoints_resource = EndpointsResource(req.get('cluster'))
    #     res = endpoints_resource.update_obj(req_params)
    #     return res

    @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)',
            url_name='update_endpoints')
    @api_decorator('Update Endpoints', serializer_class=serializers.UpdateResourcesSerializer)
    def do_update_yaml(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'yaml': params.get('yaml')
        }
        endpoints_resource = EndpointsResource(req.get('cluster'))
        res = endpoints_resource.update(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='delete', url_name='delete_endpoints')
    @api_decorator('Delete Endpoints', serializer_class=serializers.DeleteResourcesSerializer)
    def delete(self, req):
        params = req.get('params')
        req_params = {
            'resources': params.get('resources')
        }
        endpoints_resource = EndpointsResource(req.get('cluster'))
        res = endpoints_resource.delete(req_params)
        if not res.is_success():
            return res
        return CommonReturn(Code.SUCCESS, msg="删除成功")
