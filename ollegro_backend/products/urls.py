from django.urls import path

from products.views import CategoryView, ProductPropertyView

category_list = CategoryView.as_view(actions={
    'get': 'list',
    'post': 'create',
})
category_retrieve = CategoryView.as_view(actions={
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})


product_property_list = ProductPropertyView.as_view(actions={
    'get': 'list',
    'post': 'create',
})
product_property_retrieve = ProductPropertyView.as_view(actions={
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})


urlpatterns = [
    path('category/', category_list, name='category_list'),
    path('category/<int:pk>', category_retrieve, name='category_retrieve'),
    path('properties/', product_property_list, name='product_property_list'),
    path('properties/<int:pk>', product_property_retrieve, name='product_property_retrieve'),
]


