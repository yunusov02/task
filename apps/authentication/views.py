from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import LoginForm, RegisterForm


# Create your views here.
def login_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request, data=request.POST or None)

    if request.method == "POST":

        if form.is_valid():
            user = form.get_user()

            login(request, user)

            messages.success(request, f"Добро пожаловать, {user.full_name}!")
            next_url = request.GET.get("next", "dashboard")

            return redirect(next_url)

        else:
            messages.error(request, "Неверный email или пароль.")

    return render(request, "auth/login.html", {"form": form})


def register_view(request):

    if request.user.is_authenticated:
        return redirect("dashboard")

    form = RegisterForm(request.POST or None)

    if request.method == "POST":

        if form.is_valid():

            user = form.save()
            login(request, user)

            messages.success(request, "Аккаунт успешно создан!")

            return redirect("dashboard")

        else:
            messages.error(request, "Пожалуйста, исправьте ошибки ниже.")

    return render(request, "auth/register.html", {"form": form})


@login_required
def logout_view(request):

    if request.method == "POST":

        logout(request)
        messages.success(request, "Вы успешно вышли из системы.")

    return redirect("auth:login")
