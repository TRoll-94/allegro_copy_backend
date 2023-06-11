
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from payments import get_payment_model, RedirectNeeded
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


def payment_details(request, payment_id):
    """ payment details """
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


class PaymentResult(ViewSet):
    """ payment result """

    @action(methods=['get', 'post'], detail=True)
    def success(self, request, *args, **kwargs):
        """ success payment """
        if hasattr(request, 'data'):
            print(request.data)
        print(args, kwargs)
        return Response('ok')

    @action(methods=['get', 'post'], detail=True)
    def failure(self, request, *args, **kwargs):
        """ failure payment """
        if hasattr(request, 'data'):
            print(request.data)
        print(args, kwargs)
        return Response('fail')
