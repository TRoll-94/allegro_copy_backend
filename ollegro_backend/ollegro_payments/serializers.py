from rest_framework.serializers import ModelSerializer

from ollegro_payments.models import Payment


class PaymentSerializer(ModelSerializer):
    """ payment serializer """

    class Meta:
        """ meta """
        model = Payment
        fields = '__all__'
