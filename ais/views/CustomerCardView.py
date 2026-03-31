from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.CustomerCardSerializer import CustomerCardSerializer
from ..services.CustomerCardService import CustomerCardService


class CustomerCardListView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CustomerCardService()

    @extend_schema(
        responses={200: CustomerCardSerializer(many=True)},
        summary="List of all customer cards"
    )
    def get(self, request):
        surname = request.query_params.get('surname')
        if surname:
            data = self.service.search_by_surname(surname)
        else:
            data = self.service.get_list_of_customers()
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        request=CustomerCardSerializer,
        responses={201: CustomerCardSerializer, 400: dict},
        summary="Create a new customer card"
    )
    def post(self, request):
        serializer = CustomerCardSerializer(data=request.data)
        if serializer.is_valid():
            try:
                customer = self.service.add_customer(serializer.validated_data)
                return Response(customer, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerCardDetailView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CustomerCardService()

    @extend_schema(
        responses={200: CustomerCardSerializer, 404: dict},
        summary="Get customer card by number"
    )
    def get(self, request, card_number):
        try:
            data = self.service.get_customer_by_number(card_number)
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=CustomerCardSerializer,
        responses={200: CustomerCardSerializer, 400: dict, 404: dict},
        summary="Update customer card by number"
    )
    def put(self, request, card_number):
        serializer = CustomerCardSerializer(data=request.data)
        if serializer.is_valid():
            try:
                updated_data = self.service.update_customer(card_number, serializer.validated_data)
                return Response(updated_data, status=status.HTTP_200_OK)
            except ValueError as e:
                status_code = status.HTTP_404_NOT_FOUND if "не знайдено" in str(e) else status.HTTP_400_BAD_REQUEST
                return Response({"error": str(e)}, status=status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={204: None, 404: dict},
        summary="Delete customer card by number"
    )
    def delete(self, request, card_number):
        try:
            self.service.delete_customer(card_number)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
