from rest_framework import serializers


class CheckSummaryResponseSerializer(serializers.Serializer):
    total_sum = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_vat = serializers.DecimalField(max_digits=15, decimal_places=2)