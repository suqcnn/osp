import logging
from rest_framework import serializers

from . import ImplementSerializer

logger = logging.getLogger(__name__)


class CreateClusterSerializer(ImplementSerializer):
    name = serializers.CharField(required=True, allow_blank=False)
