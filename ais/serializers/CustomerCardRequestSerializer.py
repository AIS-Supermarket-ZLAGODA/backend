from rest_framework import serializers


class CustomerCardRequestSerializer(serializers.Serializer):
    surname = serializers.CharField(max_length=50, required=False)
    percent = serializers.IntegerField(min_value=0, max_value=100, required=False)
