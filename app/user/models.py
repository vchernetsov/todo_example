"""Re-declare default django admins to make further changes of it easier."""

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group
from django.db import models

from core.fields import UUIDPKField
from user.managers import UserManager


class User(AbstractUser):
    """Re-define User object to set uuid as PK for REST"""
    uuid = UUIDPKField()

    objects = UserManager()

    class Meta:
        app_label = 'user'


class Group(Group):
    """Re-define Group models to set uuid as PK and put it into
       the same admin label of user model"""

    uuid = UUIDPKField()

    class Meta:
        app_label = 'user'
