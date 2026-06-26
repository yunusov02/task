# forms.py
from django import forms

from apps.users.models import User

from .models import Task


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "user"]
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Название задачи",
                }
            ),
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 4,
                    "placeholder": "Подробное описание задачи...",
                }
            ),
            "user": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }
        labels = {
            "title": "Название",
            "description": "Описание",
            "user": "Назначить сотруднику",
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["user"].queryset = User.objects.filter(
            is_active=True,
        ).order_by("last_name", "first_name")

        self.fields["user"].empty_label = "— Выберите сотрудника —"
        self.fields["user"].required = False


class TaskStatusForm(forms.ModelForm):

    class Meta:
        model = Task
        fields = ["status"]
        widgets = {
            "status": forms.Select(
                attrs={
                    "class": "form-select",
                }
            ),
        }
        labels = {
            "status": "Статус",
        }
