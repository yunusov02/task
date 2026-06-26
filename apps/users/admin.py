from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        "email",
        "full_name",
        "role",
        "is_active",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
    )

    list_filter = (
        "role",
        "is_active",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )

    list_per_page = 10
