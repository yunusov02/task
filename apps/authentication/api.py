from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import generics
from rest_framework.permissions import AllowAny

from apps.users.models import User

from .serializers import RegisterSerializer


@extend_schema(
    tags=["auth"],
    summary="Регистрация пользователя",
    request=RegisterSerializer,
    responses={
        201: OpenApiResponse(
            response=RegisterSerializer,
            description="User registered successfully",
        ),
        400: OpenApiResponse(description="Validation error"),
    },
)
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
