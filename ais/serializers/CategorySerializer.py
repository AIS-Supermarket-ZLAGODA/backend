from rest_framework import serializers


class CategorySerializer(serializers.Serializer):
    category_number = serializers.IntegerField(read_only=True)
    category_name = serializers.CharField(max_length=255)