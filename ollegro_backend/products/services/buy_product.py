from decimal import Decimal

from payments import get_payment_model
from rest_framework.exceptions import ValidationError

from products.models import Product
from users.models import User

Payment = get_payment_model()


class BuyProduct:
    """ buy product """

    def __init__(self, product: Product, customer: User):
        self.product = product
        self.customer = customer
        self.total_units = 1

    def buy(self):
        """ buy """
        self.validate()
        self.reserve_product_units()
        payment = Payment.objects.create(
            variant='default',
            description=f'{self.customer.name}: {self.product.name}',
            customer=self.customer,
            product=self.product,
            total=self.product.price * self.total_units,
            count=self.total_units,
            tax=Decimal(0),
            currency='PLN',
            delivery=Decimal(0),
            billing_first_name=self.customer.name or self.customer.email,
            billing_last_name=self.customer.surname or '',
            billing_address_1='Default address',
            billing_address_2='',
            billing_city='Poland',
            billing_postcode='123-45',
            billing_country_code='PL',
            billing_country_area='Warsaw',
            customer_ip_address='127.0.0.1',
        )
        return payment.get_url_to_payment()

    def reserve_product_units(self):
        """ reserve product units """
        self.product.total -= self.total_units
        self.product.total_reserved += self.total_units
        self.product.save()

    def validate(self):
        """ validate purchase """
        self.availability_validation()

    def availability_validation(self):
        """ availability validation """
        if self.product.total < self.total_units:
            raise ValidationError(detail='No need stock quantity')
