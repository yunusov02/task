from django.urls import path

from .views import (task_change_status_view, task_create_view,
                    task_delete_view, task_edit_view, task_list_view)

app_name = "tasks"

urlpatterns = [
    path("", task_list_view, name="list"),
    path("create/", task_create_view, name="create"),
    path("<uuid:pk>/edit/", task_edit_view, name="edit"),
    path("<uuid:pk>/delete/", task_delete_view, name="delete"),
    path("<uuid:pk>/change_status/", task_change_status_view, name="change_status"),
]
