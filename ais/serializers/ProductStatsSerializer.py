from rest_framework import serializers

class ProductStatsRequestSerializer(serializers.Serializer):
    date_from = serializers.DateTimeField(required=False, allow_null=True)
    date_to = serializers.DateTimeField(required=False, allow_null=True)

class ProductStatsResponseSerializer(serializers.Serializer):
    id_product = serializers.IntegerField()
    total_sold = serializers.IntegerField()