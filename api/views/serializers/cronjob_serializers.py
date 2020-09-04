import logging

from rest_framework import serializers

from api.views.serializers import ImplementSerializer

logger = logging.getLogger(__name__)


class GetCronJobSerializer(ImplementSerializer):
    output = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class UpdateCronJobObjSerializer(ImplementSerializer):
    replicas = serializers.IntegerField(required=False)
