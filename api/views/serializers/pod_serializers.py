import logging

from rest_framework import serializers

from api.views.serializers import ImplementSerializer

logger = logging.getLogger(__name__)


class GetPodSerializer(ImplementSerializer):
    output = serializers.CharField(required=False, allow_blank=False)


class ExecPodSerializer(ImplementSerializer):
    container = serializers.CharField(required=True)


class PodStdinSerializer(ImplementSerializer):
    session_id = serializers.CharField(required=True)
    input = serializers.CharField(required=True)
