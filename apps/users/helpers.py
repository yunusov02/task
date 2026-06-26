from functools import wraps

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect

from .models import UserRole


def manager_required(view_func):
    """Allow only MANAGER role users."""

    @wraps(view_func)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != UserRole.MANAGER:
            messages.error(request, "У вас нет доступа к этому разделу.")
            return redirect("dashboard")
        return view_func(request, *args, **kwargs)

    return wrapper
