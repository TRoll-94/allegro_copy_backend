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
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category_id', 'code', 'name', 'value']

    def get_permissions(self):
        """ perm """
        if self.request.method in SAFE_METHODS:
            return AllowAny(),
        if action == RestActions.destroy.value:
            return isProductPropertyEmpty(), IsMerchant()
        return IsMerchant(),


class ProductView(ModelViewSet):
    """ product view """
    lookup_field = 'pk'

    @action(methods=['get'], detail=False)
    def list_sku(self, request, *args, **kwargs):
        """ list by sku """
        return super(ProductView, self).list(request, *args, **kwargs)

    @action(methods=['get'], detail=True)
    def retrieve_sku(self, request, *args, **kwargs):
        """ products by sku """
        return super(ProductView, self).retrieve(request, *args, **kwargs)

    @action(methods=['post'], detail=True)
    def buy_product(self, request, *args, **kwargs):
        """ buy product """
        product = self.get_object()
        service = BuyProduct(product, request.user)
        url_to_pay = service.buy()
        return Response({'result': url_to_pay}, status=status.HTTP_201_CREATED)

    def create(self, request, *args, **kwargs):
        """ perform create """
        request.data['owner'] = request.user.id
        return super(ProductView, self).create(request, *args, **kwargs)

    def get_queryset(self):
        """ get queryset """
        if self.action in ['list_sku', 'retrieve_sku']:
            self.lookup_field = 'sku'
            return Product.objects.values('sku').annotate(products=ArrayAgg('id'), total=Sum('total'))
        if self.request.method in SAFE_METHODS:
            return Product.objects.all()
        return Product.objects.all()

    def get_serializer_class(self):
        """ get serializer """
        if self.action in ['list_sku', 'retrieve_sku']:
            return ProductBySkuSerializer
        if self.request and self.request.method in SAFE_METHODS or self.action == 'buy_product':
            return ProductSerializer
        return ProductCreateSerializer

    def get_permissions(self):
        """ get perm """
        if self.request.method in SAFE_METHODS or self.action == 'buy_product':
            return AllowAny(),
        elif self.action in [RestActions.destroy.value, RestActions.partial_update.value]:
            return IsProductOwner(), IsMerchant()
        return IsMerchant(),


class LotView(ModelViewSet):
    """ lot view """
    queryset = Lot.objects.all()
    serializer_class = LotSerializer

    def create(self, request, *args, **kwargs):
        """ perform create """
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
        """ get perm """
        if self.request.method in SAFE_METHODS or self.action == 'buy_product':
            return AllowAny(),
        elif self.action in [RestActions.destroy.value, RestActions.partial_update.value]:
            return IsProductOwner(), IsMerchant()
        return IsMerchant(),


class RateView(ModelViewSet):
    """ rate view """
    queryset = Rate.objects.all()
    serializer_class = RateSerializer

    def create(self, request, *args, **kwargs):
        """ perform create """
        request.data['customer'] = request.user.id
        return super(RateView, self).create(request, *args, **kwargs)

    def get_permissions(self):
        """ get perm """
        if self.action in [RestActions.destroy.value, RestActions.partial_update.value]:
            return IsAdminUser(),
        return IsAuthenticated(),


