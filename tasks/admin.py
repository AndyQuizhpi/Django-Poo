from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Configuración del modelo Task en el panel de administración."""
    list_display = ('title', 'user', 'important', 'created', 'datecompleted')
    list_filter = ('important', 'datecompleted')
    search_fields = ('title', 'description', 'user__username')
    readonly_fields = ('created',)
