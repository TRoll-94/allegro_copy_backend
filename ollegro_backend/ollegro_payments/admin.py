from django.contrib import admin

# Register your models here.
from ollegro_payments.models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """ payment admin """
    list_display = [f.name for f in Payment._meta.get_fields()]
