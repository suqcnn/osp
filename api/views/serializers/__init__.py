from rest_framework import serializers


class ImplementSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class GeneralSerializer(ImplementSerializer):
    name = serializers.CharField(required=False, allow_blank=True)
    namespace = serializers.CharField(required=False, allow_blank=True)


class DeleteResourcesSerializer(ImplementSerializer):
    resources = serializers.ListField(child=GeneralSerializer(), allow_empty=True)


class UpdateResourcesSerializer(ImplementSerializer):
    yaml = serializers.CharField(required=True, allow_blank=False)
    kind = serializers.CharField(required=False, allow_blank=False)


class GetResourceSerializer(ImplementSerializer):
    output = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    kind = serializers.CharField(required=False, allow_blank=True, allow_null=True)
