from rest_framework import serializers

class BezukhAnalysisRequestSerializer(serializers.Serializer):
    date_from = serializers.DateTimeField(required=False, allow_null=True)
    date_to = serializers.DateTimeField(required=False, allow_null=True)

class BezukhAnalysisSerializer(serializers.Serializer):
    category_name = serializers.CharField()
    product_name = serializers.CharField()
    total_quantity_sold = serializers.IntegerField()
    product_revenue = serializers.DecimalField(max_digits=13, decimal_places=4)
    total_category_revenue = serializers.DecimalField(max_digits=13, decimal_places=4)

class BezukhCategoriesWithOnlyPromotionalProductsSerializer(serializers.Serializer):
    category_number = serializers.IntegerField()
    category_name = serializers.CharField()

class ZmeulProducerPerformanceRequestSerializer(serializers.Serializer):
    category_name = serializers.CharField()
    date_from = serializers.DateTimeField(required=False, allow_null=True)
    date_to = serializers.DateTimeField(required=False, allow_null=True)

class ZmeulProducerPerformanceSerializer(serializers.Serializer):
    producer = serializers.CharField()
    total_items_sold = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=13, decimal_places=4)

class ZmeulUniversalCategoriesSerializer(serializers.Serializer):
    category_number = serializers.IntegerField()
    category_name = serializers.CharField()