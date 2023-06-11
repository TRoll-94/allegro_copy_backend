from django.urls import path

from products.views import CategoryView, ProductPropertyView, ProductView

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

product_list = ProductView.as_view(actions={
    'get': 'list',
    'post': 'create',
})
product_retrieve = ProductView.as_view(actions={
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})


urlpatterns = [
    path('', product_list, name='product_list'),
    path('<int:pk>', product_retrieve, name='product_retrieve'),
    path('sku/', ProductView.as_view({'get': 'list_sku'})),
    path('sku/<int:sku>', ProductView.as_view({'get': 'retrieve_sku'})),
    path('category/', category_list, name='category_list'),
    path('category/<int:pk>', category_retrieve, name='category_retrieve'),
    path('properties/', product_property_list, name='product_property_list'),
    path('properties/<int:pk>', product_property_retrieve, name='product_property_retrieve'),
]
