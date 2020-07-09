from rest_framework import serializers


class ImplementSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class GeneralSerializer(ImplementSerializer):
    name = serializers.CharField(required=False, allow_blank=True)
    namespace = serializers.CharField(required=False, allow_blank=True)
