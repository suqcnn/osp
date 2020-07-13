import logging

from django.http import HttpResponse
from rest_framework import viewsets

from api.views import api_decorator
from api.views.serializers import cluster_serializers
from models import const
from models.cluster import Cluster
from utils import CommonReturn, Code

logger = logging.getLogger(__name__)


class ClusterViewSet(viewsets.GenericViewSet):

    @api_decorator('Create cluster', serializer_class=cluster_serializers.CreateClusterSerializer)
    def create(self, req):
        params = req.get('params')
        cluster = Cluster(params.get('name'))
        cluster.save()
        return CommonReturn(Code.SUCCESS, '添加成功')

    @api_decorator('Get cluster')
    def retrieve(self, req):
        return CommonReturn(Code.SUCCESS)

    @api_decorator('List cluster')
    def list(self, _):
        clusters = Cluster.filter()
        data = []
        for cluster in clusters:
            data.append({
                'name': cluster.name,
                'token': cluster.token,
                'create_time': cluster.create_time,
                'update_time': cluster.update_time
            })
        return CommonReturn(Code.SUCCESS, data=data)


def agent(req):
    try:
        token = req.GET.get('token')
        if not token:
            return HttpResponse("Token is blank")
        clusters = Cluster.filter(token=token)
        if len(clusters) < 1 or len(clusters) > 1:
            return HttpResponse("Not found cluster with token %s" % token)
        agent_yaml = const.agent_yaml.replace('${token}', token)
        return HttpResponse(agent_yaml)
    except Exception as exc:
        logger.error('get agent yaml error: %s' % exc, exc_info=True)
        return HttpResponse(str(exc), status=500)
