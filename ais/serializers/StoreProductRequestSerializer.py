from rest_framework import serializers


class StoreProductRequestSerializer(serializers.Serializer):
    product_name = serializers.CharField(required=False)
    order_by_products_number = serializers.BooleanField(required=False)
    promotional_product_filter = serializers.BooleanField(required=False, allow_null=True)
