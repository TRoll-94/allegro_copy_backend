from django.db.models import Count
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
        sku = data.get('sku')
        category_id = data.get('category_id')
        owner_id = data.get('owner_id')
        properties = data.get('properties', [])

        # Validate a product with the same SKU and properties
        with_same_sku_and_properties = Product.objects.filter(sku=sku, properties__in=properties)
        if self.instance:
            with_same_sku_and_properties = with_same_sku_and_properties.exclude(id=self.instance.id)
        if with_same_sku_and_properties.exists():
            raise serializers.ValidationError('Product with the same SKU and properties already exists.')

        # Check for duplicate property codes
        property_codes = [prop.code for prop in data.get('properties', [])]
        if len(property_codes) != len(set(property_codes)):
            raise serializers.ValidationError('Duplicate property codes found in the product.')

        # Checking a product with the same SKU in different categories
        with_difference_categories = Product.objects.filter(sku=sku).exclude(category_id=category_id)
        if with_difference_categories.exists():
            raise serializers.ValidationError('Duplicate SKU in different categories.')

        # Checking a product with the same SKU from different owners
        with_difference_users = Product.objects.filter(sku=sku).exclude(owner_id=owner_id)
        if with_difference_users.exists():
            raise serializers.ValidationError('Duplicate SKU among different users.')

        # Check if properties belong to the selected category
        properties_count = ProductProperty.objects.filter(id__in=properties).values('category_id').annotate(
            count=Count('id'))
        for property_count in properties_count:
            if property_count['category_id'] != category_id or property_count['count'] != len(properties):
                raise serializers.ValidationError(
                    'One or more product properties do not belong to the selected category.')

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
    """ product serializer """

    class Meta:
        """ meta """
        model = Product
        fields = '__all__'


class ProductBySkuSerializer(serializers.ModelSerializer):
    """ Serializer for products by sku """
    sku = serializers.CharField()
    total = serializers.IntegerField()
    category = serializers.SerializerMethodField()
    products = serializers.SerializerMethodField()

    def get_products(self, value):
        """ products """
        data = Product.objects.filter(id__in=value['products'])
        return ProductSerializer(instance=data, many=True).data

    def get_category(self, value):
        """ category """
        category = Category.objects.filter(products__in=value['products']).last()
        return CategorySerializer(instance=category).data

    class Meta:
        """ Meta """
        model = Product
        fields = ['sku', 'total', 'category', 'products']
