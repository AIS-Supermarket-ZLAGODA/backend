from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.CheckSerializer import CheckSerializer, CheckCreateSerializer
from ..services.CheckService import CheckService


class CheckListView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CheckService()

    @extend_schema(
        responses={200: CheckSerializer(many=True)},
        summary="List of all checks"
    )
    def get(self, request):
        id_employee = request.query_params.get('id_employee')
        data = self.service.get_list_of_checks(id_employee=id_employee)
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
