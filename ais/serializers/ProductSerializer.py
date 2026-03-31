from rest_framework import serializers

class ProductSerializer(serializers.Serializer):
    id_product = serializers.IntegerField(read_only=True)
    category_number = serializers.IntegerField()
    product_name = serializers.CharField(max_length=50)
    producer = serializers.CharField(max_length=50)
    characteristics = serializers.CharField(max_length=100)