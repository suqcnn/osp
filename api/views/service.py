import logging
from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator, serializers
from api.views.serializers import service_serializers
from service.kuberesource.service import ServiceResource
from utils import CommonReturn, Code

logger = logging.getLogger(__name__)


class ServiceViewSet(viewsets.GenericViewSet):

    @api_decorator('List Services', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        service_resource = ServiceResource(req.get("cluster"))
        query_params = {}
        if params.get('name'):
            query_params['name'] = params.get('name')
        if params.get('namespace'):
            query_params['namespace'] = params.get('namespace')
        res = service_resource.list(query_params)
        if not res.data:
            res.data = []
        return res

    @action(methods=['GET'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)', url_name='get_service')
    @api_decorator('Get Service', serializer_class=service_serializers.GetServiceSerializer)
    def get(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'output': params.get('output')
        }
        service_resource = ServiceResource(req.get('cluster'))
        res = service_resource.get(req_params)
        return res

    # @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)/update_obj',
    #         url_name='update_Service_obj')
    # @api_decorator('Update Service', serializer_class=service_serializers.UpdateServiceObjSerializer)
    # def update_obj(self, req):
    #     params = req.get('params')
    #     req_params = {
    #         'name': req.get('name'),
    #         'namespace': req.get('namespace'),
    #         'replicas': params.get('replicas')
    #     }
    #     service_resource = ServiceResource(req.get('cluster'))
    #     res = service_resource.update_obj(req_params)
    #     return res

    @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)',
            url_name='update_Service')
    @api_decorator('Update Service', serializer_class=serializers.UpdateResourcesSerializer)
    def do_update_yaml(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'yaml': params.get('yaml')
        }
        service_resource = ServiceResource(req.get('cluster'))
        res = service_resource.update(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='delete', url_name='delete_services')
    @api_decorator('Delete Services', serializer_class=serializers.DeleteResourcesSerializer)
    def delete(self, req):
        params = req.get('params')
        req_params = {
            'resources': params.get('resources')
        }
        service_resource = ServiceResource(req.get('cluster'))
        res = service_resource.delete(req_params)
        if not res.is_success():
            return res
        return CommonReturn(Code.SUCCESS, msg="删除成功")
