from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.StoreProductSerializer import StoreProductSerializer
from ..services.StoreProductService import StoreProductService


class StoreProductListView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = StoreProductService()

    @extend_schema(
        responses={200: StoreProductSerializer(many=True)},
        summary="List of all store products"
    )
    def get(self, request):
        product_name = request.query_params.get('product_name')
        if product_name:
            data = self.service.search_by_product_name(product_name)
        else:
            data = self.service.get_list_of_store_products()
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        request=StoreProductSerializer,
        responses={201: StoreProductSerializer, 400: dict},
        summary="Create a new store product"
    )
    def post(self, request):
        serializer = StoreProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                store_product = self.service.add_store_product(serializer.validated_data)
                return Response(store_product, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StoreProductDetailView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = StoreProductService()

    @extend_schema(
        responses={200: StoreProductSerializer, 404: dict},
        summary="Get store product by UPC"
    )
    def get(self, request, UPC):
        try:
            data = self.service.get_store_product_by_upc(UPC)
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=StoreProductSerializer,
        responses={200: StoreProductSerializer, 400: dict, 404: dict},
        summary="Update store product by UPC"
    )
    def put(self, request, UPC):
        serializer = StoreProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                updated_data = self.service.update_store_product(UPC, serializer.validated_data)
                return Response(updated_data, status=status.HTTP_200_OK)
            except ValueError as e:
                status_code = status.HTTP_404_NOT_FOUND if "не знайдено" in str(e) else status.HTTP_400_BAD_REQUEST
                return Response({"error": str(e)}, status=status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={204: None, 404: dict},
        summary="Delete store product by UPC"
    )
    def delete(self, request, UPC):
        try:
            self.service.delete_store_product(UPC)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
