from drf_spectacular.utils import OpenApiResponse, extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from apps.users.permissions import ManagerRequiredPermission

from .models import Task
from .serializers import TaskSerializer


@extend_schema(
    responses={
        200: TaskSerializer,
        400: OpenApiResponse(description="Bad request"),
    }
)
class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.select_related("user", "created_by").all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, ManagerRequiredPermission]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
