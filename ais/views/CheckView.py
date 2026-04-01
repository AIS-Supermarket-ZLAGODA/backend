from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.CheckRequestSerializer import CheckRequestSerializer
from ..serializers.CheckSerializer import CheckSerializer, CheckCreateSerializer
from ..services.CheckService import CheckService


class CheckListView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CheckService()

    @extend_schema(
        parameters=[CheckRequestSerializer],
        responses={200: CheckSerializer(many=True)},
        summary="List of checks with filters (by employee and/or date range)"
    )
    def get(self, request):
        query_params = CheckRequestSerializer(data=request.query_params)
        query_params.is_valid(raise_exception=True)

        params = query_params.validated_data

        data = self.service.get_list_of_checks(
            id_employee=params.get('id_employee'),
            date_from=params.get('date_from'),
            date_to=params.get('date_to')
        )
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        request=CheckCreateSerializer,
        responses={201: CheckSerializer, 400: dict},
        summary="Create a new check with sale items"
    )
    def post(self, request):
        serializer = CheckCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                check = self.service.create_check(
                    id_employee=serializer.validated_data['id_employee'],
                    card_number=serializer.validated_data.get('card_number'),
                    items=serializer.validated_data['items'],
                )
                return Response(check, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckDetailView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CheckService()

    @extend_schema(
        responses={200: CheckSerializer, 404: dict},
        summary="Get check by number"
    )
    def get(self, request, check_number):
        try:
            data = self.service.get_check_by_number(check_number)
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        responses={204: None, 404: dict},
        summary="Delete check by number"
    )
    def delete(self, request, check_number):
        try:
            self.service.delete_check(check_number)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)


class CheckSummaryView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CheckService()

    @extend_schema(
        parameters=[CheckRequestSerializer],
        responses={200: dict},
        summary="Get total sales sum and VAT summary for a period/employee"
    )
    def get(self, request):
        query_params = CheckRequestSerializer(data=request.query_params)
        query_params.is_valid(raise_exception=True)

        params = query_params.validated_data

        summary = self.service.get_checks_summary(
            id_employee=params.get('id_employee'),
            date_from=params.get('date_from'),
            date_to=params.get('date_to')
        )
        return Response(summary, status=status.HTTP_200_OK)