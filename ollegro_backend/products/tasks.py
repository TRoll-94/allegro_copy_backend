from django.utils import timezone

from ollegro_backend.celery import app
from products.models import Lot


@app.task(name="products.tasks.close_overdue_lot")
def close_lot(**kwargs):
    lot_id = kwargs['lot_id']
    lot = Lot.objects.filter(id=lot_id).first()
    if lot is None:
        return
    current_time = timezone.now()
    if lot.end_at <= current_time:
        max_rate = lot.rates.order_by('sum', 'created_at').last()
        if max_rate is None:
            lot.status = Lot.LotStatuses.FAIL
        elif max_rate.sum < lot.sale_price:
            lot.status = Lot.LotStatuses.FAIL
        else:
            lot.status = Lot.LotStatuses.CLOSED
            lot.final_rate = max_rate
        lot.save()
    else:
        remaining_time = lot.end_at - current_time
        countdown = remaining_time.total_seconds()+1
        app.send_task("products.tasks.close_overdue_lot", kwargs={'lot_id': lot_id}, countdown=countdown)

    print('Here in lot overdue check # 1')