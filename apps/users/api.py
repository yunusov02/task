from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import User
from .permissions import ManagerRequiredPermission
from .serializers import UserSerializer


@extend_schema(
    responses={
        200: OpenApiResponse(response=UserSerializer),
        201: OpenApiResponse(response=UserSerializer),
        400: OpenApiResponse(response=UserSerializer),
    }
)
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, ManagerRequiredPermission]

    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .filter(is_active=True)
            .order_by("last_name", "first_name")
        )

    def perform_create(self, serializer):
        serializer.save(is_active=True)
