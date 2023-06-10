from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Sum
from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import AllowAny, SAFE_METHODS

from ollegro_backend.consts import RestActions
from products.license import IsMerchant, IsCategoryEmpty, isProductPropertyEmpty, IsProductOwner
from products.models import Category, ProductProperty, Product
from products.serializers import CategorySerializer, ProductPropertySerializer, ProductCreateSerializer, \
    ProductSerializer, ProductBySkuSerializer


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


class ProductView(ModelViewSet):
    """ product view """

    def create(self, request, *args, **kwargs):
        """ perform create """
        request.data['owner'] = request.user.id
        return super(ProductView, self).create(request, *args, **kwargs)

    def get_queryset(self):
        """ get queryset """
        if self.request.method in SAFE_METHODS:
            return Product.objects.values('sku').annotate(products=ArrayAgg('id'), total=Sum('total'))
        return Product.objects.all()

    def get_serializer_class(self):
        """ get serializer """
        if self.request.method in SAFE_METHODS:
            return ProductBySkuSerializer
        return ProductCreateSerializer

    def get_permissions(self):
        """ get perm """
        if self.request.method in SAFE_METHODS:
            return AllowAny(),
        elif self.action in [RestActions.destroy.value, RestActions.partial_update.value]:
            return IsProductOwner(), IsMerchant()
        return IsMerchant(),
