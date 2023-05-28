from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.viewsets import ModelViewSet

from ollegro_backend.license import IsObjectOwner
from users.models import User
from users.serializers import UserSerializer


class UserModelView(ModelViewSet):
    """ user view set """
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        """ perform update """
        if 'password' in serializer.validated_data:
            password = make_password(serializer.validated_data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    def get_permissions(self):
        """ get permissions """
        if self.action == 'create':
            return AllowAny(),
        if self.request.method in SAFE_METHODS:
            return IsAuthenticated(),
        else:
            return IsObjectOwner(),

    def get_queryset(self):
        """ return user """
        self.kwargs['pk'] = self.request.user.id
        return User.objects.filter(id=self.request.user.id)
