import logging
from rest_framework import viewsets

from api.views import api_decorator
from service.kuberesource.event import EventResource
from api.views.serializers import event_serializers

logger = logging.getLogger(__name__)


class EventViewSet(viewsets.GenericViewSet):

    @api_decorator('List events', serializer_class=event_serializers.ListEventSerializer)
    def list(self, req):
        params = req.get('params')
        event_resource = EventResource(req.get("cluster"))
        query_params = {}
        if params.get('uid'):
            query_params['uid'] = params.get('uid')
        if params.get('kind'):
            query_params['kind'] = params.get('kind')
        if params.get('name'):
            query_params['name'] = params.get('name')
        if params.get('namespace'):
            query_params['namespace'] = params.get('namespace')
        res = event_resource.list(query_params)
        if not res.data:
            res.data = []
        return res
