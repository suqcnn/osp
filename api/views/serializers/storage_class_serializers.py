import logging

from rest_framework import serializers

from api.views.serializers import ImplementSerializer, GeneralSerializer

logger = logging.getLogger(__name__)


class GetStorageClassSerializer(ImplementSerializer):
    output = serializers.CharField(required=False, allow_blank=True, allow_null=True)

