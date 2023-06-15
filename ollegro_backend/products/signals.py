from django.db.models.signals import post_save
from django.dispatch import receiver

from products.models import Lot


# @receiver(post_save, sender=Lot)
# def update_lot(sender, instance: Lot, created, **kwargs):
#     """ update lot """
#     max_rate = instance.rates.order_by('sum', 'created_at').last()
#     if max_rate is not None and max_rate.sum >= instance.sale_price:
#         instance.status = Lot.LotStatuses.CLOSED
#         instance.final_rate = max_rate
#         instance.save()
#         return
#
#     if instance.status == Lot.LotStatuses.CLOSED and instance.final_rate is not None:
#         return
#
#     if instance.status == Lot.LotStatuses.CLOSED:
#         instance.final_rate = max_rate
#         instance.save()
