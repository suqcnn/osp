import logging
from rest_framework import viewsets
from rest_framework.decorators import action

from api.views import api_decorator, serializers
from api.views.serializers import ingress_serializers
from service.kuberesource.ingress import IngressResource
from utils import CommonReturn, Code

logger = logging.getLogger(__name__)


class IngressViewSet(viewsets.GenericViewSet):

    @api_decorator('List Ingresses', serializer_class=serializers.GeneralSerializer)
    def list(self, req):
        params = req.get('params')
        ingress_resource = IngressResource(req.get("cluster"))
        query_params = {}
        if params.get('name'):
            query_params['name'] = params.get('name')
        if params.get('namespace'):
            query_params['namespace'] = params.get('namespace')
        res = ingress_resource.list(query_params)
        if not res.data:
            res.data = []
        return res

    @action(methods=['GET'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)', url_name='get_ingress')
    @api_decorator('Get Ingress', serializer_class=ingress_serializers.GetIngressSerializer)
    def get(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'output': params.get('output')
        }
        ingress_resource = IngressResource(req.get('cluster'))
        res = ingress_resource.get(req_params)
        return res

    # @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)/update_obj',
    #         url_name='update_Ingress_obj')
    # @api_decorator('Update Ingress', serializer_class=ingress_serializers.UpdateIngressObjSerializer)
    # def update_obj(self, req):
    #     params = req.get('params')
    #     req_params = {
    #         'name': req.get('name'),
    #         'namespace': req.get('namespace'),
    #         'replicas': params.get('replicas')
    #     }
    #     ingress_resource = IngressResource(req.get('cluster'))
    #     res = ingress_resource.update_obj(req_params)
    #     return res

    @action(methods=['POST'], detail=False, url_path='(?P<namespace>[^/.]+)/(?P<name>[^/.]+)',
            url_name='update_Ingress')
    @api_decorator('Update Ingress', serializer_class=serializers.UpdateResourcesSerializer)
    def do_update_yaml(self, req):
        params = req.get('params')
        req_params = {
            'name': req.get('name'),
            'namespace': req.get('namespace'),
            'yaml': params.get('yaml')
        }
        ingress_resource = IngressResource(req.get('cluster'))
        res = ingress_resource.update(req_params)
        return res

    @action(methods=['POST'], detail=False, url_path='delete', url_name='delete_ingresses')
    @api_decorator('Delete Ingresses', serializer_class=serializers.DeleteResourcesSerializer)
    def delete(self, req):
        params = req.get('params')
        req_params = {
            'resources': params.get('resources')
        }
        ingress_resource = IngressResource(req.get('cluster'))
        res = ingress_resource.delete(req_params)
        if not res.is_success():
            return res
        return CommonReturn(Code.SUCCESS, msg="删除成功")
