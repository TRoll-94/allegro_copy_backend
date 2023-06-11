
from django.urls import include, path
from ollegro_payments.views import PaymentResult, payment_details

urlpatterns = [
    path('<int:payment_id>', payment_details),
    path('<int:pk>/success', PaymentResult.as_view({'post': 'success'})),
    path('<int:pk>/failure', PaymentResult.as_view({'post': 'failure'})),
    path('', include('payments.urls'))
]
