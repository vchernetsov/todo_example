from django.db import models


class UserManager(models.Manager):
    def rendered(self):
        return self.filter(is_active=True, is_superuser=False)
