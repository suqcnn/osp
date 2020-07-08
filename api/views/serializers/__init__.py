from rest_framework import serializers


class GeneralSerializer(serializers.Serializer):
    cluster = serializers.CharField(required=True, allow_blank=False)
    namespace = serializers.CharField(required=False, allow_blank=True)
