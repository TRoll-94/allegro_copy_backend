from django.urls import path

from products.views import CategoryView


category_list = CategoryView.as_view(actions={
    'get': 'list',
    'post': 'create',
})
category_retrieve = CategoryView.as_view(actions={
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})


urlpatterns = [
    path('category/', category_list, name='category_list'),
    path('category/<int:pk>', category_retrieve, name='category_retrieve'),
]


