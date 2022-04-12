from django.contrib.admin import ModelAdmin

from core.admin import admin
from todo import models


class TaskAdmin(ModelAdmin):
    list_display = (
        'owner',
        'name',
        'status',
    )
    list_filter = (
        'owner',
        'status',
    )
    readonly_fields = (
        'created_at',
        'owner',
    )


admin.register(models.Task, TaskAdmin)
