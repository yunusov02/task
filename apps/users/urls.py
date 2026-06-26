from django.urls import path

from .views import (user_create_view, user_delete_view, user_detail_view,
                    user_edit_view, user_list_view)

app_name = "employees"


urlpatterns = [
    path("", user_list_view, name="list"),
    path("create/", user_create_view, name="create"),
    path("<uuid:pk>/", user_detail_view, name="detail"),
    path("<uuid:pk>/edit/", user_edit_view, name="edit"),
    path("<uuid:pk>/delete/", user_delete_view, name="delete"),
]
