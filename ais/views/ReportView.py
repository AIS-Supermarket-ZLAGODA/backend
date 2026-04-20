from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.ReportSerializer import BezukhAnalysisRequestSerializer, BezukhAnalysisSerializer, \
    BezukhCategoriesWithOnlyPromotionalProductsSerializer, ZmeulProducerPerformanceRequestSerializer, \
    ZmeulProducerPerformanceSerializer, ZmeulUniversalCategoriesSerializer, \
    LapkoCustomerSpendingRequestSerializer, LapkoCategoryRequestSerializer
from ..services.ReportService import BezukhReportService, ZmeulReportService, LapkoReportService


class BezukhReportAnalysisView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = BezukhReportService()

    @extend_schema(
        parameters=[BezukhAnalysisRequestSerializer],
        responses={200: BezukhAnalysisSerializer(many=True)},
        summary="Analysis for all categories"
    )
    def get(self, request):
        query_params = BezukhAnalysisRequestSerializer(data=request.query_params)
        query_params.is_valid(raise_exception=True)

        params = query_params.validated_data

        data = self.service.get_sales_analysis_report(
            date_from=params.get('date_from'),
            date_to=params.get('date_to')
        )

        return Response(data, status=status.HTTP_200_OK)

class BezukhReportPromotionalCategoriesView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = BezukhReportService()

    @extend_schema(
        responses={200: BezukhCategoriesWithOnlyPromotionalProductsSerializer(many=True)},
        summary="Categories with only promotional products"
    )
    def get(self, request):
        data = self.service.get_categories_with_only_promotional_products()
        return Response(data, status=status.HTTP_200_OK)

class ZmeulProducerPerformanceView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ZmeulReportService()

    @extend_schema(
        parameters=[ZmeulProducerPerformanceRequestSerializer],
        responses={200: ZmeulProducerPerformanceSerializer(many=True), 400: dict},
        summary="Producer performance analysis inside a category"
    )
    def get(self, request):
        query_params = ZmeulProducerPerformanceRequestSerializer(data=request.query_params)
        if not query_params.is_valid():
            return Response(query_params.errors, status=status.HTTP_400_BAD_REQUEST)

        params = query_params.validated_data
        
        try:
            data = self.service.get_producer_performance(
                category_name=params.get('category_name'),
                date_from=params.get('date_from'),
                date_to=params.get('date_to')
            )
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ZmeulUniversalCategoriesView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ZmeulReportService()

    @extend_schema(
        responses={200: ZmeulUniversalCategoriesSerializer(many=True)},
        summary="Categories where absolutely every cashier has sold at least one product"
    )
    def get(self, request):
        data = self.service.get_universal_categories()
        return Response(data, status=status.HTTP_200_OK)


class LapkoCustomerSpendingView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = LapkoReportService()

    @extend_schema(
        parameters=[LapkoCustomerSpendingRequestSerializer],
        summary="Per-customer totals (checks, items, spending) inside a category and period"
    )
    def get(self, request):
        query_params = LapkoCustomerSpendingRequestSerializer(data=request.query_params)
        if not query_params.is_valid():
            return Response(query_params.errors, status=status.HTTP_400_BAD_REQUEST)

        params = query_params.validated_data
        try:
            data = self.service.get_customers_category_spending(
                category_name=params.get('category_name'),
                date_from=params.get('date_from'),
                date_to=params.get('date_to')
            )
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class LapkoCustomersBoughtAllView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = LapkoReportService()

    @extend_schema(
        parameters=[LapkoCategoryRequestSerializer],
        summary="Customers who bought at least one of every product in the given category"
    )
    def get(self, request):
        query_params = LapkoCategoryRequestSerializer(data=request.query_params)
        if not query_params.is_valid():
            return Response(query_params.errors, status=status.HTTP_400_BAD_REQUEST)

        params = query_params.validated_data
        try:
            data = self.service.get_customers_bought_all_in_category(
                category_name=params.get('category_name')
            )
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)