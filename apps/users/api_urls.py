from rest_framework.routers import DefaultRouter

from .api import UserViewSet

app_name = "users_api"

router = DefaultRouter()
router.register("users", UserViewSet, basename="user")

urlpatterns = router.urls
