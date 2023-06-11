from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class IsPurchaseOwner(BasePermission):
    """ is purchase owner """

    def has_object_permission(self, request, view, obj):
        """ perm """
        if request.user == obj.customer:
            return True
        raise PermissionDenied(detail="it's not good to spy on other people's purchases")


