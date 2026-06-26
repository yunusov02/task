from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from django.shortcuts import render

from apps.tasks.models import Task, TaskStatus
from apps.users.models import User, UserRole


@login_required
def dashboard_view(request):

    context = {}

    if request.user.role == UserRole.MANAGER:
        total_employees = User.objects.filter(
            role=UserRole.EMPLOYEE, is_active=True
        ).count()

        task_stats = Task.objects.aggregate(
            total=Count("id"),
            created=Count("id", filter=Q(status=TaskStatus.CREATED)),
            in_progress=Count("id", filter=Q(status=TaskStatus.IN_PROGRESS)),
            done=Count("id", filter=Q(status=TaskStatus.DONE)),
            cancelled=Count("id", filter=Q(status=TaskStatus.CANCELLED)),
        )

        recent_tasks = Task.objects.select_related("user", "created_by").order_by(
            "-created_at"
        )[:8]

        context.update(
            {
                "total_employees": total_employees,
                "task_stats": task_stats,
                "recent_tasks": recent_tasks,
                "is_manager": True,
            }
        )

    else:
        # Employee sees only their tasks
        my_tasks = Task.objects.filter(user=request.user).order_by("-created_at")

        my_stats = {
            "total": my_tasks.count(),
            "created": my_tasks.filter(status=TaskStatus.CREATED).count(),
            "in_progress": my_tasks.filter(status=TaskStatus.IN_PROGRESS).count(),
            "done": my_tasks.filter(status=TaskStatus.DONE).count(),
        }

        context.update(
            {
                "my_tasks": my_tasks[:10],
                "my_stats": my_stats,
                "is_manager": False,
            }
        )

    return render(request, "dashboard.html", context)
