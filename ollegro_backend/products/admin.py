from django.contrib import admin

from products.models import Category, ProductProperty, Product, Lot, Rate

admin.site.register(Category)
admin.site.register(ProductProperty)
admin.site.register(Product)
admin.site.register(Lot)
admin.site.register(Rate)


# Register your models here.
