from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from ..serializers.CategorySerializer import CategorySerializer
from ..services.CategoryService import CategoryService


class CategoryListView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CategoryService()

    @extend_schema(
        responses={200: CategorySerializer(many=True)},
        summary="List of all categories"
    )
    def get(self, request):
        data = self.service.get_list_of_categories()
        return Response(data, status=status.HTTP_200_OK)

    @extend_schema(
        request=CategorySerializer,
        responses={201: CategorySerializer, 400: dict},
        summary="Create a new category"
    )
    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            try:
                new_id = self.service.add_category(serializer.validated_data['category_name'])

                response_data = {
                    "category_number": new_id,
                    "category_name": serializer.validated_data['category_name']
                }
                return Response(response_data, status=status.HTTP_201_CREATED)

            except ValueError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = CategoryService()

    @extend_schema(
        responses={200: CategorySerializer, 404: dict},
        summary="Get category by number"
    )
    def get(self, request, category_number):
        try:
            data = self.service.get_category_by_number(category_number)
            return Response(data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        request=CategorySerializer,
        responses={200: CategorySerializer, 400: dict, 404: dict},
        summary="Update category by number"
    )
    def put(self, request, category_number):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            try:
                updated_data = self.service.update_category(
                    category_number,
                    serializer.validated_data['category_name']
                )
                return Response(updated_data, status=status.HTTP_200_OK)
            except ValueError as e:
                status_code = status.HTTP_404_NOT_FOUND if "not found" in str(e) else status.HTTP_400_BAD_REQUEST
                return Response({"error": str(e)}, status=status_code)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @extend_schema(
        responses={204: None, 404: dict},
        summary="Delete category by number"
    )
    def delete(self, request, category_number):
        try:
            self.service.delete_category(category_number)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)