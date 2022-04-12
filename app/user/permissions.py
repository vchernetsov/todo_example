from django.utils.translation import gettext_lazy as _
from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Permission to check if user is an owner"""

    message = _('You must be an owner in order to perform this action')

    def has_object_permission(self, request, view, obj):
        """Check that user is an owner"""
        return obj == request.user
