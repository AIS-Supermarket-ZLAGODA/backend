from rest_framework import serializers

class CheckRequestSerializer(serializers.Serializer):
    id_employee = serializers.CharField(required=False, allow_null=True)
    date_from = serializers.DateTimeField(required=False, allow_null=True)
    date_to = serializers.DateTimeField(required=False, allow_null=True)