import logging

from rest_framework import serializers

from api.views.serializers import ImplementSerializer, GeneralSerializer

logger = logging.getLogger(__name__)


class GetPodSerializer(ImplementSerializer):
    output = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class ListPodSerializer(GeneralSerializer):
    label_selector = serializers.DictField(required=False, allow_null=True)
