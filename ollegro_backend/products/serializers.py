from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from products.models import ProductProperty, Category, Product


class CategorySerializer(serializers.ModelSerializer):
    """ Serializer for category model """

    class Meta:
        """ Meta """
        model = Category
        fields = '__all__'


class ProductPropertySerializer(serializers.ModelSerializer):
    """ Serializer for products properties """
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        """ Meta """
        model = ProductProperty
        fields = "__all__"
        extra_kwargs = {
            'name': {'required': True},
            'code': {'required': True},
            'value': {'required': True},
        }


class ProductCreateSerializer(serializers.ModelSerializer):
    """ Serializer for products categories """
    properties = serializers.PrimaryKeyRelatedField(queryset=ProductProperty.objects.all(), many=True)

    def validate(self, data):
        """
        validate
        """
        products_with_same_sku_and_properties = Product.objects.filter(sku=data['sku'],
                                                                       properties__in=data['properties'])
        if self.instance:
            products_with_same_sku_and_properties = products_with_same_sku_and_properties.exclude(id=self.instance.id)

        if products_with_same_sku_and_properties.exists():
            raise ValidationError(detail='Product with the same SKU and properties already exists.')

        property_codes = [prop.code for prop in data.get('properties', [])]
        if len(property_codes) != len(set(property_codes)):
            raise serializers.ValidationError('Duplicate property codes found in the product.')

        return data

    class Meta:
        """ Meta """
        model = Product
        fields = '__all__'
        extra_kwargs = {
            'name': {'required': True},
            'description': {'required': True},
            'price': {'required': True},
            'total': {'required': True},
            'sku': {'required': True},
        }


class ProductSerializer(serializers.ModelSerializer):
    """ Serializer for products categories """
    properties = ProductPropertySerializer(many=True)

    class Meta:
        """ Meta """
        model = Product
        fields = '__all__'
