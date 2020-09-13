import logging

from rest_framework import serializers

from api.views.serializers import ImplementSerializer, GeneralSerializer

logger = logging.getLogger(__name__)


class GetIngressSerializer(ImplementSerializer):
    output = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class UpdateIngressObjSerializer(ImplementSerializer):
    replicas = serializers.IntegerField(required=False)
