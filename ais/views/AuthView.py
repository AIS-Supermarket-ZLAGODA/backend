from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import status, serializers
from rest_framework.views import APIView
from rest_framework.response import Response

from ..services.AuthService import AuthService


class LoginView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.service = AuthService()

    @extend_schema(
        request=inline_serializer(
            name="LoginRequest",
            fields={
                "login": serializers.CharField(),
                "password": serializers.CharField(),
            }
        ),
        responses={
            200: inline_serializer(
                name="LoginResponse",
                fields={
                    "id_employee": serializers.CharField(),
                    "empl_name": serializers.CharField(),
                    "empl_surname": serializers.CharField(),
                    "empl_role": serializers.CharField(),
                    "token": serializers.CharField(),
                }
            ),
            400: inline_serializer(
                name="LoginError",
                fields={"error": serializers.CharField()}
            ),
        },
        summary="Login with employee ID or phone + password"
    )
    def post(self, request):
        login = request.data.get("login", "").strip()
        password = request.data.get("password", "")

        if not login or not password:
            return Response(
                {"error": "Логін та пароль обов'язкові"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_data = self.service.authenticate(login, password)
            # Simple token: employee ID (placeholder until JWT is added)
            user_data["token"] = user_data["id_employee"]
            return Response(user_data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
