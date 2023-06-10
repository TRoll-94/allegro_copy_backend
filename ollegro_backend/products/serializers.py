
from rest_framework import serializers

from products.models import ProductProperty, Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """ Serializer for category model """

    class Meta:
        """ Meta """
        model = Category
        fields = '__all__'


class ProductPropertySerializer(serializers.ModelSerializer):
    """ Serializer for products properties """

    class Meta:
        """ Meta """
        model = ProductProperty
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    """ Serializer for products categories """

    class Meta:
        """ Meta """
        model = Product
        fields = '__all__'
