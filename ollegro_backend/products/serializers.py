from gettext import Catalog

from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    """ Serializer for category model """

    class Meta:
        """ Meta """
        fields = '__all__'
        model = Catalog


