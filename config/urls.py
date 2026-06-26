from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path

from .views import dashboard_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard_view, name="dashboard"),
    path("user/", include("apps.users.urls")),
    path("auth/", include("apps.authentication.urls")),
    path("task/", include("apps.tasks.urls")),
]

urlpatterns += staticfiles_urlpatterns()
