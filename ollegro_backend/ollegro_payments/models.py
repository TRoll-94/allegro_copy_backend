from decimal import Decimal
from typing import Iterable

from payments import PurchasedItem
from payments.models import BasePayment


class Payment(BasePayment):
    """ payment model """

    def get_failure_url(self):
        """ fail url """
        return f'http://localhost:8000/api/payments/{self.pk}/failure'

    def get_success_url(self):
        """ success url """
        return f'http://localhost:8000/api/payments/{self.pk}/success'

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
