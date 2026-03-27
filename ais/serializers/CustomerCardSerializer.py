from rest_framework import serializers


class CustomerCardSerializer(serializers.Serializer):
    card_number = serializers.CharField(read_only=True)
    cust_surname = serializers.CharField(max_length=50)
    cust_name = serializers.CharField(max_length=50)
    cust_patronymic = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    phone_number = serializers.CharField(max_length=13)
    city = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    street = serializers.CharField(max_length=50, required=False, allow_blank=True, allow_null=True)
    zip_code = serializers.CharField(max_length=9, required=False, allow_blank=True, allow_null=True)
    percent = serializers.IntegerField()
