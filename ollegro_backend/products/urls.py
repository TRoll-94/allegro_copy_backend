from django.urls import path

from products.views import CategoryView, ProductPropertyView, ProductView, LotView, RateView

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

lot_list = LotView.as_view(actions={
    'get': 'list',
    'post': 'create',
})
lot_retrieve = LotView.as_view(actions={
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})

rate_list = RateView.as_view(actions={
    'get': 'list',
    'post': 'create',
})
rate_retrieve = RateView.as_view(actions={
    'get': 'retrieve',
    'patch': 'partial_update',
    'delete': 'destroy',
})

urlpatterns = [
    path('', product_list, name='product_list'),
    path('<int:pk>', product_retrieve, name='product_retrieve'),
    path('buy/<int:pk>', ProductView.as_view({'post': 'buy_product'}), name='product_buy'),
    path('sku/', ProductView.as_view({'get': 'list_sku'})),
    path('sku/<int:sku>', ProductView.as_view({'get': 'retrieve_sku'})),
    path('category/', category_list, name='category_list'),
    path('category/<int:pk>', category_retrieve, name='category_retrieve'),
    path('properties/', product_property_list, name='product_property_list'),
    path('lot/<int:pk>', lot_retrieve, name='lot_retrieve'),
    path('lot/', lot_list, name='lot_list'),
    path('rate/<int:pk>', rate_retrieve, name='rate_retrieve'),
    path('rate/', rate_list, name='rate_list'),
]
