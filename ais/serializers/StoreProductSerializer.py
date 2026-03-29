from rest_framework import serializers


class StoreProductSerializer(serializers.Serializer):
    UPC = serializers.CharField(max_length=12)
    UPC_prom = serializers.CharField(max_length=12, required=False, allow_blank=True, allow_null=True)
    id_product = serializers.IntegerField()
    selling_price = serializers.DecimalField(max_digits=13, decimal_places=4)
    products_number = serializers.IntegerField()
    promotional_product = serializers.BooleanField()
    product_name = serializers.CharField(read_only=True, required=False)
