from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.users.helpers import manager_required
from apps.users.models import User, UserRole

from .forms import TaskForm, TaskStatusForm
from .models import Task, TaskStatus


@login_required
def task_list_view(request):

    if request.user.role == UserRole.MANAGER:
        queryset = Task.objects.select_related("user", "created_by").all()
    else:
        queryset = Task.objects.select_related("user", "created_by").filter(
            user=request.user
        )

    q = request.GET.get("q", "").strip()

    if q:
        queryset = queryset.filter(Q(title__icontains=q) | Q(description__icontains=q))

    status_filter = request.GET.get("status", "")

    if status_filter in TaskStatus.values:
        queryset = queryset.filter(status=status_filter)

    employee_filter = request.GET.get("employee", "")

    if employee_filter and request.user.role == UserRole.MANAGER:
        queryset = queryset.filter(user__pk=employee_filter)

    queryset = queryset.order_by("-created_at")

    base_qs = (
        Task.objects.all()
        if request.user.role == UserRole.MANAGER
        else Task.objects.filter(user=request.user)
    )

    stats = base_qs.aggregate(
        total=Count("id"),
        created=Count("id", filter=Q(status=TaskStatus.CREATED)),
        in_progress=Count("id", filter=Q(status=TaskStatus.IN_PROGRESS)),
        done=Count("id", filter=Q(status=TaskStatus.DONE)),
        cancelled=Count("id", filter=Q(status=TaskStatus.CANCELLED)),
    )

    # Pagination
    paginator = Paginator(queryset, 10)
    page = request.GET.get("page", 1)
    tasks = paginator.get_page(page)

    employees = (
        User.objects.filter(is_active=True).order_by("last_name")
        if request.user.role == UserRole.MANAGER
        else []
    )

    return render(
        request,
        "tasks/list.html",
        {
            "tasks": tasks,
            "stats": stats,
            "employees": employees,
            "statuses": TaskStatus.choices,
            "q": q,
            "status_filter": status_filter,
            "employee_filter": employee_filter,
            "is_manager": request.user.role == UserRole.MANAGER,
        },
    )


@login_required
def task_detail_view(request, pk):

    if request.user.role == UserRole.MANAGER:

        task = get_object_or_404(Task, pk=pk)
    else:

        task = get_object_or_404(Task, pk=pk, user=request.user)

    return render(request, "tasks/detail.html", {"task": task})


@manager_required
def task_create_view(request):

    form = TaskForm(request.POST or None)

    if request.method == "POST":
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.status = TaskStatus.CREATED
            task.save()
            messages.success(request, f"Задача «{task.title}» создана!")
            return redirect("tasks:list")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки ниже.")

    preselect_employee = request.GET.get("employee")

    if preselect_employee and request.method != "POST":
        form.initial["user"] = preselect_employee

    return render(
        request,
        "tasks/create.html",
        {
            "form": form,
            "preselect_employee": preselect_employee,
        },
    )


@login_required
def task_edit_view(request, pk):

    # manager can edit any task
    # employee can only edit their own tasks

    if request.user.role == UserRole.MANAGER:

        task = get_object_or_404(Task, pk=pk)
        FormClass = TaskForm
    else:

        task = get_object_or_404(Task, pk=pk, user=request.user)
        FormClass = TaskStatusForm

    form = FormClass(request.POST or None, instance=task)

    if request.method == "POST":
        if form.is_valid():
            form.save()

            messages.success(request, f"Задача «{task.title}» обновлена.")

            return redirect("tasks:list")
        else:
            messages.error(request, "Пожалуйста, исправьте ошибки ниже.")

    return render(
        request,
        "tasks/edit.html",
        {
            "form": form,
            "task": task,
            "is_manager": request.user.role == UserRole.MANAGER,
        },
    )


@manager_required
def task_delete_view(request, pk):
    task = get_object_or_404(Task, pk=pk)

    if request.method == "POST":
        title = task.title
        task.delete()
        messages.success(request, f"Задача «{title}» удалена.")
        return redirect("tasks:list")

    return render(request, "tasks/confirm_delete.html", {"task": task})


@login_required
def task_change_status_view(request, pk):
    if request.user.role == UserRole.MANAGER:
        task = get_object_or_404(Task, pk=pk)
    else:
        task = get_object_or_404(Task, pk=pk, user=request.user)

    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in TaskStatus.values:
            task.status = new_status
            task.save(update_fields=["status"])
            messages.success(request, f"Статус задачи «{task.title}» изменён.")
        else:
            messages.error(request, "Неверный статус.")

    return redirect(request.META.get("HTTP_REFERER", "tasks:list"))
