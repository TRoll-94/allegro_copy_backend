from decimal import Decimal
from typing import Iterable

from payments import PurchasedItem
from payments.models import BasePayment
from django.db import models

from products.models import Product
from users.models import User


class Payment(BasePayment):
    """ payment model """
    customer = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='purchases', verbose_name='Customer')
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name='purchases', verbose_name='Product')
    count = models.PositiveIntegerField(verbose_name='Count of products units', default=1)

    def get_failure_url(self):
        """ fail url """
        return f'http://localhost:8000/api/payments/{self.pk}/failure'

    def get_success_url(self):
        """ success url """
        return f'http://localhost:8000/api/payments/{self.pk}/success'

    def get_url_to_payment(self):
        """ payment url """
        return f'http://localhost:8000/api/payments/{self.pk}'

    def get_purchased_items(self) -> Iterable[PurchasedItem]:
        """ items    """
        # you'll probably want to retrieve these from an associated order
        yield PurchasedItem(
            name='The Hound of the Baskervilles',
            sku='BSKV',
            quantity=9,
            price=Decimal(10),
            currency='USD',
        )

    def release(self):
        """ release """
        self.product.total_reserved -= self.count
        self.product.save()
        super(Payment, self).release()

