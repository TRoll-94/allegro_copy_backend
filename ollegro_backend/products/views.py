from rest_framework.decorators import action
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import AllowAny, SAFE_METHODS

from ollegro_backend.consts import RestActions
from products.license import IsMerchant, IsCategoryEmpty
from products.models import Category
from products.serializers import CategorySerializer


class CategoryView(ModelViewSet):
    """ category view """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        """ perm """
        if self.action in RestActions.safe():
            return AllowAny(),
        if self.action == RestActions.destroy.value:
            return IsCategoryEmpty(), IsMerchant()
        return IsMerchant(),
