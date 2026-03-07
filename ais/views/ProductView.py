from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.ProductSerializer import ProductSerializer
from ..services.ProductService import ProductService

class ProductListView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProductService()

    @extend_schema(responses={200: ProductSerializer(many=True)},
                   summary="List all products (filter by category_name or product_name)")
    def get(self, request):
        category_name = request.GET.get('category_name')
        product_name = request.GET.get('product_name')

        data = self.service.get_list_of_products(category_name=category_name, product_name=product_name)
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(request=ProductSerializer, responses={201: ProductSerializer, 400: dict},
                   summary="Create a new product")
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                new_id = self.service.add_product(
                    serializer.validated_data['category_number'],
                    serializer.validated_data['product_name'],
                    serializer.validated_data['producer'],
                    serializer.validated_data['characteristics']
                )
                response_data = {"id_product": new_id, **serializer.validated_data}
                return Response(response_data, status=status.HTTP_201_CREATED)
            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductDetailView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = ProductService()

    @extend_schema(responses={200: ProductSerializer, 404: dict}, summary="Get product by ID")
    def get(self, request, id_product):
        try:
            data = self.service.get_product_by_id(id_product)
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(request=ProductSerializer, responses={200: ProductSerializer, 400: dict, 404: dict},
                   summary="Update product by ID")
    def put(self, request, id_product):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            try:
                updated_data = self.service.update_product(
                    id_product,
                    serializer.validated_data['category_number'],
                    serializer.validated_data['product_name'],
                    serializer.validated_data['producer'],
                    serializer.validated_data['characteristics']
                )
                return Response(updated_data, status=status.HTTP_200_OK)
            except ValueError as e:
                status_code = status.HTTP_404_NOT_FOUND if "not found" in str(e) else status.HTTP_400_BAD_REQUEST
                return Response({"error": str(e)}, status=status_code)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(responses={204: None, 400: dict, 404: dict}, summary="Delete product by ID")
    def delete(self, request, id_product):
        try:
            self.service.delete_product(id_product)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            status_code = status.HTTP_400_BAD_REQUEST if "cannot be deleted" in str(e) else status.HTTP_404_NOT_FOUND
            return Response({"error": str(e)}, status=status_code)