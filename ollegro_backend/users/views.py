from django.contrib.auth.hashers import make_password
from rest_framework.permissions import AllowAny, IsAuthenticated, SAFE_METHODS
from rest_framework.viewsets import ModelViewSet

from ollegro_backend.license import IsObjectOwner
from users.models import User
from users.serializers import UserSerializer


class UserModelView(ModelViewSet):
    """
    View for managing user accounts.

    Attributes:
    - serializer_class: The serializer for user objects.

    Methods:
    - perform_update: Perform update, hash the password if it is provided.
    - get_permissions: Get permissions based on the request method and action.
    - get_queryset: Get queryset to return user information.
    """
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        """
        Perform update on user object.

        Parameters:
        - serializer: The serializer instance.

        Notes:
        - If 'password' is provided in the data, hash the password before saving.
        """
        if 'password' in serializer.validated_data:
            password = make_password(serializer.validated_data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    def get_permissions(self):
        """
        Get permissions based on the request method and action.

        Returns:
        - Tuple of permissions.
        """
        if self.action == 'create':
            return AllowAny(),
        if self.request.method in SAFE_METHODS:
            return IsAuthenticated(),
        else:
            return IsObjectOwner(),

    def get_queryset(self):
        """
        Get queryset to return user information.

        Returns:
        - Queryset of the authenticated user.
        """
        self.kwargs['pk'] = self.request.user.id
        return User.objects.filter(id=self.request.user.id)
