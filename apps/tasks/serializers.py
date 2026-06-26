from rest_framework import serializers

from apps.users.serializers import UserReadSerializer

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    user_detail = UserReadSerializer(source="user", read_only=True)
    created_by_detail = UserReadSerializer(source="created_by", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "status",
            "user",
            "user_detail",
            "created_by",
            "created_by_detail",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_by", "created_at", "updated_at"]
