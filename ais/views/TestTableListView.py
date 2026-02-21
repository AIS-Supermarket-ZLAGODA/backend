from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.TestTableSerializer import TestTableSerializer
from ..services.TestTableService import TestTableService


class TestTableListView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = TestTableService()

    @extend_schema(
        responses={200: TestTableSerializer(many=True)},
        summary="Список тестів",
        description="Отримує дані через Service -> Repo -> SQL."
    )
    def get(self, request):
        data = self.service.get_list_of_tests()
        return Response(data)

    @extend_schema(
        request=TestTableSerializer,
        responses={201: TestTableSerializer},
        summary="Створити запис",
        description="Додає новий запис у test_table через Raw SQL."
    )
    def post(self, request):
        serializer = TestTableSerializer(data=request.data)
        if serializer.is_valid():
            new_id = self.service.add_test_entry(serializer.validated_data['full_name'])
            return Response({"id": new_id, **serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)