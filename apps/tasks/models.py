from django.db import models

from apps.users.models import User
from config.basemodel import BaseModel


class TaskStatus(models.TextChoices):
    CREATED = "CREATED", "Created"
    IN_PROGRESS = "IN_PROGRESS", "In Progress"
    DONE = "DONE", "Done"
    CANCELLED = "CANCELLED", "Cancelled"


class Task(BaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(
        max_length=20, choices=TaskStatus.choices, default=TaskStatus.CREATED
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="created_tasks"
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = "tasks"
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
