from django.conf import settings
from rest_framework.permissions import BasePermission

User = settings.AUTH_USER_MODEL


class IsObjectOwner(BasePermission):
    """ Return True if user is superuser or object owner """

    def has_object_permission(self, request, view, obj):
        """ has object permissions """
        if obj == request.user:
            return True
        if hasattr(obj, 'user') and obj.user == request.user:
            return True
        if request.user.is_superuser:
            return True

        return False
