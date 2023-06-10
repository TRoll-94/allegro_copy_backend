from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import AllowAny, SAFE_METHODS

from ollegro_backend.consts import RestActions
from products.license import IsMerchant, IsCategoryEmpty, isProductPropertyEmpty
from products.models import Category, ProductProperty
from products.serializers import CategorySerializer, ProductPropertySerializer


class CategoryView(ModelViewSet):
    """ category view """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        """ perm """
        if self.request.method in SAFE_METHODS:
            return AllowAny(),
        if self.action == RestActions.destroy.value:
            return IsCategoryEmpty(), IsMerchant()
        return IsMerchant(),


class ProductPropertyView(ModelViewSet):
    """ product property view """
    queryset = ProductProperty.objects.all()
    serializer_class = ProductPropertySerializer

    def get_permissions(self):
        """ perm """
        if self.request.method in SAFE_METHODS:
            return AllowAny(),
        if action == RestActions.destroy.value:
            return isProductPropertyEmpty(), IsMerchant()
        return IsMerchant(),

