from django.contrib import admin


from .models import Task

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    
    list_display = (
        "title",
        "description",
        "status",
    )
    
    list_filter = (
        "status",
    )
    
    search_fields = (
        "title",
        "description",
    )
    
    readonly_fields = (
        "created_at",
        "updated_at",
    )
    
    list_per_page = 10
    
    
    