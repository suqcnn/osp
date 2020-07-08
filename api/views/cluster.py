import logging

from rest_framework import viewsets

from api.views import api_decorator
from api.views.serializers import cluster_serializers
from models.cluster import Cluster
from utils import CommonReturn, Code

logger = logging.getLogger(__name__)


class ClusterViewSet(viewsets.GenericViewSet):

    @api_decorator('Create cluster', serializer_class=cluster_serializers.CreateClusterSerializer)
    def create(self, request, params):
        cluster = Cluster(params.get('name'))
        cluster.save()
        return CommonReturn(Code.SUCCESS, '添加成功')

    @api_decorator('Get cluster')
    def retrieve(self, request, pk):
        return CommonReturn(Code.SUCCESS)

    @api_decorator('List cluster')
    def list(self, request):
        return CommonReturn(Code.SUCCESS)
