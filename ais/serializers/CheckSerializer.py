from rest_framework import serializers


class SaleItemSerializer(serializers.Serializer):
    UPC = serializers.CharField(max_length=12)
    product_number = serializers.IntegerField(min_value=1)


class CheckCreateSerializer(serializers.Serializer):
    id_employee = serializers.CharField(max_length=10)
    card_number = serializers.CharField(max_length=13, required=False, allow_blank=True, allow_null=True)
    items = SaleItemSerializer(many=True)


class SaleSerializer(serializers.Serializer):
    UPC = serializers.CharField()
    check_number = serializers.CharField()
    product_number = serializers.IntegerField()
    selling_price = serializers.DecimalField(max_digits=13, decimal_places=4)
    product_name = serializers.CharField(read_only=True, required=False)


class CheckSerializer(serializers.Serializer):
    check_number = serializers.CharField()
    id_employee = serializers.CharField()
    card_number = serializers.CharField(allow_null=True)
    print_date = serializers.DateTimeField()
    sum_total = serializers.DecimalField(max_digits=13, decimal_places=4)
    vat = serializers.DecimalField(max_digits=13, decimal_places=4)
    empl_surname = serializers.CharField(read_only=True, required=False)
    empl_name = serializers.CharField(read_only=True, required=False)
    items = SaleSerializer(many=True, read_only=True, required=False)
