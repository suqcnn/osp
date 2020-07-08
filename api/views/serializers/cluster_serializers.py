import logging
from rest_framework import serializers

logger = logging.getLogger(__name__)


class CreateClusterSerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False)
