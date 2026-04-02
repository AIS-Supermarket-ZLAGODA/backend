from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from ..serializers.ReportSerializer import BezukhAnalysisRequestSerializer, BezukhAnalysisSerializer, \
    BezukhCategoriesWithOnlyPromotionalProductsSerializer
from ..services.ReportService import BezukhReportService


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