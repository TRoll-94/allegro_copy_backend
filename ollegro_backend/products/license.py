from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied

from products.models import Category, ProductProperty
from users.consts import DefaultUserTypes


class IsCategoryEmpty(BasePermission):
    """ category is empty """

    def has_object_permission(self, request, view, obj: Category):
        """ has perm """
        products = obj.products.count()
        properties = obj.properties.count()
        if products == 0 and properties == 0:
            return True
        raise PermissionDenied(detail='Category is not empty')


class isProductPropertyEmpty(BasePermission):
    """ product property is empty """

    def has_object_permission(self, request, view, obj: ProductProperty):
        """ has perm """
        product = obj.products.count()
        if product == 0:
            return True
        raise PermissionDenied(detail='Product property is not empty')


class IsMerchant(BasePermission):
    """ member is merchant """

    def has_object_permission(self, request, view, obj):
        """ perm """
        if request.user.is_superuser:
            return True

        return request.user.user_type.code == DefaultUserTypes.merchant.value

    def has_permission(self, request, view):
        """ perm """

        if request.user.is_superuser:
            return True

        return request.user.user_type.code == DefaultUserTypes.merchant.value


class IsCustomer(BasePermission):
    """ member is customer """

    def has_object_permission(self, request, view, obj):
        """ perm """
        if request.user.is_superuser:
            return True

        return request.user.user_type.code == DefaultUserTypes.customer.value

    def has_permission(self, request, view):
        """ perm """

        if request.user.is_superuser:
            return True

        return request.user.user_type.code == DefaultUserTypes.customer.value
