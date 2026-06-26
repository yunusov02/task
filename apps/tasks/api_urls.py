from rest_framework.routers import DefaultRouter

from .api import TaskViewSet

app_name = "tasks_api"

router = DefaultRouter()
router.register("tasks", TaskViewSet, basename="task")

urlpatterns = router.urls
