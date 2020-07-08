import logging
from rest_framework import serializers

from api.views.serializers import GeneralSerializer


logger = logging.getLogger(__name__)


class ListPodSerializer(GeneralSerializer):
    name = serializers.CharField(required=False, allow_blank=True)
