from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import Sum
from django.utils import timezone
from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import AllowAny, SAFE_METHODS, IsAuthenticated, IsAdminUser

from ollegro_backend.celery import app
from ollegro_backend.consts import RestActions
from products.license import IsMerchant, IsCategoryEmpty, isProductPropertyEmpty, IsProductOwner
from products.models import Category, ProductProperty, Product, Lot, Rate
from products.serializers import CategorySerializer, ProductPropertySerializer, ProductCreateSerializer, \
    ProductSerializer, ProductBySkuSerializer, LotSerializer, RateSerializer
from products.services.buy_product import BuyProduct


class CategoryView(ModelViewSet):
    """
    View for managing product categories.

    Attributes:
    - queryset: The set of all categories.
    - serializer_class: The serializer for categories.

    Methods:
    - get_permissions: Returns permissions based on the request method.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        """
        Returns permissions based on the request method.
        """
        if self.request.method in SAFE_METHODS:
            return AllowAny(),
        if self.action == RestActions.destroy.value:
            return IsCategoryEmpty(), IsMerchant()
        return IsMerchant(),


class ProductPropertyView(ModelViewSet):
    """
    View for managing product properties.

    Attributes:
    - queryset: The set of all product properties.
    - serializer_class: The serializer for product properties.
    - filter_backends: The backend filters for product properties.
    - filterset_fields: The fields to filter product properties.

    Methods:
    - get_permissions: Returns permissions based on the request method.
    """
    queryset = ProductProperty.objects.all()
    serializer_class = ProductPropertySerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category_id', 'code', 'name', 'value']

    def get_permissions(self):
        """
        Returns permissions based on the request method.
        """
        if self.request.method in SAFE_METHODS:
            return AllowAny(),
        if action == RestActions.destroy.value:
            return isProductPropertyEmpty(), IsMerchant()
        return IsMerchant(),


class ProductView(ModelViewSet):
    """
    View for managing products.

    Attributes:
    - lookup_field: The field to look up products.

    Methods:
    - list_sku: Retrieve a list of products grouped by SKU.
    - retrieve_sku: Retrieve detailed information about products by SKU.
    - buy_product: Buy a product.
    - create: Perform product creation.
    - get_queryset: Get queryset based on the action.
    - get_serializer_class: Get serializer class based on the action and request method.
    - get_permissions: Get permissions based on the request method and action.
    """
    lookup_field = 'pk'

    @action(methods=['get'], detail=False)
    def list_sku(self, request, *args, **kwargs):
        """
        Retrieve a list of products grouped by SKU.
        """
        return super(ProductView, self).list(request, *args, **kwargs)

    @action(methods=['get'], detail=True)
    def retrieve_sku(self, request, *args, **kwargs):
        """
        Retrieve detailed information about products by SKU.
        """
        return super(ProductView, self).retrieve(request, *args, **kwargs)

    @action(methods=['post'], detail=True)
    def buy_product(self, request, *args, **kwargs):
        """
        Buy a product.
        """
        product = self.get_object()
        service = BuyProduct(product, request.user)
        url_to_pay = service.buy()
        return Response({'result': url_to_pay}, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        """
        Perform product creation.
        """
        print(request.user)

        request.data['owner'] = request.user.id
        request.data['owner_id'] = request.user.id
        print(request.data['owner'])
        print(request.data['owner_id'])

        return super(ProductView, self).create(request, *args, **kwargs)

    def get_queryset(self):
        """
        Get queryset based on the action.
        """
        if self.action in ['list_sku', 'retrieve_sku']:
            self.lookup_field = 'sku'
            return Product.objects.values('sku').annotate(products=ArrayAgg('id'), total=Sum('total'))
        if self.request.method in SAFE_METHODS:
            return Product.objects.all()
        return Product.objects.all()

    def get_serializer_class(self):
        """
        Get serializer class based on the action and request method.
        """
        if self.action in ['list_sku', 'retrieve_sku']:
            return ProductBySkuSerializer
        if self.request and self.request.method in SAFE_METHODS or self.action == 'buy_product':
            return ProductSerializer
        return ProductCreateSerializer

    def get_permissions(self):
        """
        Get permissions based on the request method and action.
        """
        if self.request.method in SAFE_METHODS or self.action == 'buy_product':
            return AllowAny(),
        elif self.action in [RestActions.destroy.value, RestActions.partial_update.value]:
            return IsProductOwner(), IsMerchant()
        return IsMerchant(),


class LotView(ModelViewSet):
    """
    View for managing lots.

    Attributes:
    - queryset: The set of all lots.
    - serializer_class: The serializer for lots.

    Methods:
    - create: Perform lot creation.
    - get_permissions: Get permissions based on the request method and action.
    """
    queryset = Lot.objects.all()
    serializer_class = LotSerializer

    def create(self, request, *args, **kwargs):
        """
        Perform lot creation.
        """
        request.data['owner'] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        result = serializer.data
        lot = Lot.objects.get(id=result['id'])
        current_time = timezone.now()
        remaining_time = lot.end_at - current_time
        countdown = remaining_time.total_seconds()+1
        app.send_task("products.tasks.close_overdue_lot", kwargs={'lot_id': result['id']}, countdown=countdown)
        return Response(result, status=status.HTTP_201_CREATED, headers=headers)

    def get_permissions(self):
        """
        Get permissions based on the request method and action.
        """
        if self.request.method in SAFE_METHODS or self.action == 'buy_product':
            return AllowAny(),
        elif self.action in [RestActions.destroy.value, RestActions.partial_update.value]:
            return IsProductOwner(), IsMerchant()
        return IsMerchant(),


class RateView(ModelViewSet):
    """
    View for managing rates.

    Attributes:
    - queryset: The set of all rates.
    - serializer_class: The serializer for rates.

    Methods:
    - create: Perform rate creation.
    - get_permissions: Get permissions based on the request method and action.
    """
    queryset = Rate.objects.all()
    serializer_class = RateSerializer

    def create(self, request, *args, **kwargs):
        """
        Perform rate creation.
        """
        request.data['customer'] = request.user.id
        return super(RateView, self).create(request, *args, **kwargs)

    def get_permissions(self):
        """
        Get permissions based on the request method and action.
        """
        if self.action in [RestActions.destroy.value, RestActions.partial_update.value]:
            return IsAdminUser(),
        return IsAuthenticated(),


