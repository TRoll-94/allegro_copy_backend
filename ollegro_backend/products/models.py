from django.db import models

from users.models import User


class Category(models.Model):
    """ Category """
    name = models.CharField(max_length=32, verbose_name='Category name')

    def __str__(self):
        return self.name


class Product(models.Model):
    """ products """
    name = models.CharField(max_length=32, verbose_name='Product name')
    description = models.TextField(verbose_name='Product description')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='Product category')
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Product owner')
    total = models.IntegerField(verbose_name='Total products')
    total_reserved = models.IntegerField(verbose_name='Reserved products')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

