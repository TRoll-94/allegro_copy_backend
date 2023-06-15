from django.core.exceptions import ValidationError
from django.db import models

from users.models import User
from django.utils.translation import gettext_lazy as _



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
        unique_together = ('code', 'value', 'category')


class Product(models.Model):
    """ products """
    name = models.CharField(max_length=32, verbose_name='Product name')
    description = models.TextField(verbose_name='Product description')
    category = models.ForeignKey(
        Category, on_delete=models.DO_NOTHING, related_name='products', verbose_name='Product category'
    )
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Price')
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Product owner')
    total = models.IntegerField(verbose_name='Total products')
    total_reserved = models.IntegerField(verbose_name='Reserved products', default=0)
    sku = models.CharField(verbose_name='Product code')
    properties = models.ManyToManyField(ProductProperty, related_name='products', verbose_name='Properties')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'


class Lot(models.Model):
    """ Lot product """

    class LotStatuses(models.TextChoices):
        """ lot statuses """
        OPEN = "OPEN", _("Open")
        PROCESS = "PROCESS", _("Process")
        CLOSED = "CLOSED", _("Closed")

    name = models.CharField(max_length=32)
    start_price = models.DecimalField(max_digits=9, decimal_places=2)
    final_rate = models.ForeignKey('Rate', on_delete=models.DO_NOTHING, related_name='final_lot', null=True, blank=True)
    sale_price = models.DecimalField(max_digits=9, decimal_places=2, default=100)
    description = models.TextField()
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    start_at = models.DateTimeField(auto_now=True)
    end_at = models.DateTimeField()
    status = models.CharField(max_length=12, choices=LotStatuses.choices, default=LotStatuses.OPEN)


class Rate(models.Model):
    """ Rate """

    sum = models.DecimalField(max_digits=9, decimal_places=2)
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    lot = models.ForeignKey(Lot, on_delete=models.DO_NOTHING)

