from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.tasks.models import Task, TaskStatus

from .forms import UserCrateForm, UserEditForm
from .helpers import manager_required
from .models import User, UserRole


@manager_required
def user_list_view(request):

    queryset = User.objects.all().order_by("last_name", "first_name")

    q = request.GET.get("q", "").strip()
    if q:
        queryset = queryset.filter(
            Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
            | Q(email__icontains=q)
            | Q(phone_number__icontains=q)
        )

    role_filter = request.GET.get("role", "")

    if role_filter in UserRole.values:
        queryset = queryset.filter(role=role_filter)

    active_filter = request.GET.get("active", "")

    if active_filter == "1":
        queryset = queryset.filter(is_active=True)
    elif active_filter == "0":
        queryset = queryset.filter(is_active=False)

    queryset = queryset.annotate(task_count=Count("task"))

    paginator = Paginator(queryset, 10)
    page = request.GET.get("page", 1)
    employees = paginator.get_page(page)

    total = User.objects.count()
    active_count = User.objects.filter(is_active=True).count()
    manager_count = User.objects.filter(role=UserRole.MANAGER).count()
    employee_count = User.objects.filter(role=UserRole.EMPLOYEE).count()
    tasks_count = Task.objects.exclude(status=TaskStatus.DONE).count()

    return render(
        request,
        "employees/list.html",
        {
            "employees": employees,
            "total": total,
            "active_count": active_count,
            "manager_count": manager_count,
            "employee_count": employee_count,
            "tasks_count": tasks_count,
            "roles": UserRole.choices,
            "q": q,
            "role_filter": role_filter,
            "active_filter": active_filter,
        },
    )


@manager_required
def user_detail_view(request, pk):
    employee = get_object_or_404(User, pk=pk)

    tasks = Task.objects.filter(user=employee).order_by("-created_at")
    task_stats = {
        "total": tasks.count(),
        "created": tasks.filter(status=TaskStatus.CREATED).count(),
        "in_progress": tasks.filter(status=TaskStatus.IN_PROGRESS).count(),
        "done": tasks.filter(status=TaskStatus.DONE).count(),
    }

    return render(
        request,
        "employees/detail.html",
        {
            "employee": employee,
            "tasks": tasks[:10],
            "task_stats": task_stats,
        },
    )


@manager_required
def user_create_view(request):
    form = UserCrateForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            employee = form.save()
            messages.success(request, f"Сотрудник {employee.full_name} успешно создан!")
            return redirect("employees:detail", pk=employee.pk)
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки ниже.")

    return render(request, "employees/create.html", {"form": form})


@manager_required
def user_edit_view(request, pk):
    employee = get_object_or_404(User, pk=pk)
    form = UserEditForm(request.POST or None, instance=employee)

    if request.method == "POST":
        if form.is_valid():
            form.save()
            messages.success(
                request, f"Данные сотрудника {employee.full_name} обновлены."
            )
            return redirect("employees:detail", pk=employee.pk)
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки ниже.")

    return render(
        request,
        "employees/edit.html",
        {
            "form": form,
            "employee": employee,
        },
    )


@manager_required
def user_delete_view(request, pk):
    employee = get_object_or_404(User, pk=pk)

    if request.method == "POST":
        name = employee.full_name
        employee.delete()
        messages.success(request, f"Сотрудник {name} удалён.")
        return redirect("employees:list")

    return render(request, "employees/confirm_delete.html", {"employee": employee})
