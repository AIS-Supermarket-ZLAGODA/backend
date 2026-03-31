from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.EmployeeSerializer import EmployeeSerializer
from ..services.EmployeeService import EmployeeService


class EmployeeListView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = EmployeeService()

    @extend_schema(
        responses={200: EmployeeSerializer(many=True)},
        summary="List of all employees"
    )
    def get(self, request):
        surname = request.query_params.get('empl_surname')
        data = self.service.get_list_of_employees(surname=surname)
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        request=EmployeeSerializer,
        responses={201: EmployeeSerializer, 400: dict},
        summary="Create a new employee"
    )
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                new_id = self.service.add_employee(serializer.validated_data)
                employee = self.service.get_employee_by_id(new_id)
                return Response(employee, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetailView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = EmployeeService()

    @extend_schema(
        responses={200: EmployeeSerializer, 404: dict},
        summary="Get employee by ID"
    )
    def get(self, request, id_employee):
        try:
            data = self.service.get_employee_by_id(id_employee)
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=EmployeeSerializer,
        responses={200: EmployeeSerializer, 400: dict, 404: dict},
        summary="Update employee by ID"
    )
    def put(self, request, id_employee):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                updated_data = self.service.update_employee(
                    id_employee,
                    serializer.validated_data
                )
                return Response(updated_data, status=status.HTTP_200_OK)
            except ValueError as e:
                status_code = (
                    status.HTTP_404_NOT_FOUND
                    if "не знайдено" in str(e)
                    else status.HTTP_400_BAD_REQUEST
                )
                return Response({"error": str(e)}, status=status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={204: None, 404: dict},
        summary="Delete employee by ID"
    )
    def delete(self, request, id_employee):
        try:
            self.service.delete_employee(id_employee)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
