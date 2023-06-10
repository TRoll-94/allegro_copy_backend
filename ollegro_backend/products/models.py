from django.db import models

from users.models import User


class Category(models.Model):
    """ Category """
    name = models.CharField(max_length=32, verbose_name='Category name')
    code = models.CharField(max_length=16, verbose_name='Category code', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class ProductProperty(models.Model):
    """ Product property """
    name = models.CharField(max_length=64, verbose_name='Property name')
    code = models.CharField(max_length=16, verbose_name='Property code')
    value = models.CharField(max_length=64, verbose_name='Property value')
    category = models.ForeignKey(
        Category, verbose_name='Category', related_name='properties', on_delete=models.DO_NOTHING
    )

    def __str__(self):
        return f"{self.name} {self.category}"

    class Meta:
        verbose_name = 'Product property'
        verbose_name_plural = 'Product properties'
        unique_together = ('code', 'category')


class Product(models.Model):
    """ products """
    name = models.CharField(max_length=32, verbose_name='Product name')
    description = models.TextField(verbose_name='Product description')
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name='products', verbose_name='Product category'
    )
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Product owner')
    total = models.IntegerField(verbose_name='Total products')
    total_reserved = models.IntegerField(verbose_name='Reserved products')
    sku = models.CharField(verbose_name='Product code')
    properties = models.ManyToManyField(ProductProperty, related_name='products', verbose_name='Properties')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

