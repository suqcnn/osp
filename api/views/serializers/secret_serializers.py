import logging

from rest_framework import serializers

from api.views.serializers import ImplementSerializer

logger = logging.getLogger(__name__)


class GetSecretSerializer(ImplementSerializer):
    output = serializers.CharField(required=False, allow_blank=True, allow_null=True)

class UpdateSecretSerializer(ImplementSerializer):
    namespace = serializers.CharField(required=True, max_length=64)
    name = serializers.CharField(required=True, max_length=64)
    yaml = serializers.CharField(required=True, allow_blank=False)
