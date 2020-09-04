import logging

from rest_framework import serializers

from api.views.serializers import ImplementSerializer, GeneralSerializer

logger = logging.getLogger(__name__)


class GetJobSerializer(ImplementSerializer):
    output = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class ListJobSerializer(GeneralSerializer):
    cronjob_uid = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class UpdateJobObjSerializer(ImplementSerializer):
    replicas = serializers.IntegerField(required=False)
