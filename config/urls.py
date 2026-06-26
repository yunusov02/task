from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from drf_spectacular.views import (SpectacularAPIView, SpectacularRedocView,
                                   SpectacularSwaggerView)

from .views import dashboard_view

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", dashboard_view, name="dashboard"),
    path("user/", include("apps.users.urls")),
    path("auth/", include("apps.authentication.urls")),
    path("task/", include("apps.tasks.urls")),
    # API
    path("api/", include("apps.authentication.api_urls")),
    path("api/", include("apps.users.api_urls")),
    path("api/", include("apps.tasks.api_urls")),
    # Swagger
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

urlpatterns += staticfiles_urlpatterns()
