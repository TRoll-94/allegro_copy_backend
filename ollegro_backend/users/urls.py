from django.urls import path
from users.views import UserModelView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

user_view_list = UserModelView.as_view(actions={
    'get': 'retrieve',
    'patch': 'partial_update',
    'post': 'create',
    'delete': 'destroy',
})

urlpatterns = [
    path('', user_view_list, name='register_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/status/', TokenVerifyView.as_view(), name='token_status'),
]
