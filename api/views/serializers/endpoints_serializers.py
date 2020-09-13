import logging

from rest_framework import serializers

from api.views.serializers import ImplementSerializer, GeneralSerializer

logger = logging.getLogger(__name__)


class GetEndpointsSerializer(ImplementSerializer):
    output = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class UpdateEndpointsObjSerializer(ImplementSerializer):
    replicas = serializers.IntegerField(required=False)
