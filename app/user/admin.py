from django.contrib.auth.admin import GroupAdmin, UserAdmin

from core.admin import admin
from user import models

admin.register(models.User, UserAdmin)
admin.register(models.Group, GroupAdmin)
