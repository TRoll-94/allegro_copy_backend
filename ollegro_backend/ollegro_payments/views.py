
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.urls import reverse
from payments import get_payment_model, RedirectNeeded, PaymentStatus
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import IsAuthenticated

from ollegro_payments.license import IsPurchaseOwner
from ollegro_payments.models import Payment
from ollegro_payments.serializers import PaymentSerializer


def payment_details(request, payment_id):
    """
    View for displaying payment details.

    Parameters:
    - payment_id: The ID of the payment to retrieve.

    Returns:
    - A template with payment details and a payment form.
    """
    payment = get_object_or_404(get_payment_model(), id=payment_id)

    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))

    return TemplateResponse(
        request,
        'payment.html',
        {'form': form, 'payment': payment}
    )


class PaymentResult(ModelViewSet):
    """
    View for handling payment results.
    """
    serializer_class = PaymentSerializer

    @action(methods=['post'], detail=True)
    def success(self, request, *args, **kwargs):
        """
        Action for successful payment.

        Returns:
        - Response indicating successful payment.
        """
        payment = self.get_object()
        return Response('ok')

    @action(methods=['post'], detail=True)
    def failure(self, request, *args, **kwargs):
        """
        Action for failed payment.

        Returns:
        - Response indicating failed payment.
        """
        payment = self.get_object()
        if payment.status == PaymentStatus.CONFIRMED:
            return self.success(request, *args, **kwargs)
        if payment.status not in [PaymentStatus.REJECTED, PaymentStatus.CONFIRMED, PaymentStatus.REFUNDED, PaymentStatus.PREAUTH]:
            payment.product.total += payment.counts
            payment.product.total_reserved -= payment.count
            payment.product.save()
            payment.status = PaymentStatus.REJECTED
            payment.save()
        return Response('fail')

    def get_permissions(self):
        """
        Get permissions for accessing payment results.

        Returns:
        - Tuple of permissions (IsAuthenticated, IsPurchaseOwner).
        """
        return IsAuthenticated(), IsPurchaseOwner()

    def get_queryset(self):
        """
        Get queryset of payments related to the authenticated user.

        Returns:
        - Queryset of payments filtered by the authenticated user and related product.
        """
        return Payment.objects.filter(customer=self.request.user).select_related('product')
