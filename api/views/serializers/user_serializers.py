import logging

from rest_framework import serializers

from api.views.serializers import ImplementSerializer

logger = logging.getLogger(__name__)


class CreateUserSerializer(ImplementSerializer):
    name = serializers.CharField(required=True, allow_blank=False)
    email = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(required=True, allow_blank=False)

class UpdateUserSerializer(ImplementSerializer):
    status = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    email = serializers.CharField(required=False, allow_blank=True, allow_null=True)

class CreateAdminSerializer(ImplementSerializer):
    password = serializers.CharField(required=True, allow_blank=False)
