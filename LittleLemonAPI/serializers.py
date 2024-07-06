from rest_framework import serializers
from LittleLemonAPI.models import *
from decimal import Decimal
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    """
    won't be used in post request. will only be used for displaying
    read_only=True

    This will only be used for price and we cant create an item with price less than 2
    price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)


    This can be used to set minimum value for the fields

    extra_kwargs = {
        'price': {'min_value': 2},
        'stock': {'source': 'inventory', 'min_value': 0}
    }

    When you want to use UniqueTogetherValidator validator, the code will be a little different.
    Here’s a sample code that will make the combination of title and price field unique.
    With this validation, there will be no duplicate entry of an item with the same price.
    This code goes directly inside the Meta class.

    validators = [
        UniqueTogetherValidator(
            queryset=MenuItem.objects.all(),
            fields=['title', 'price']
        ),
    ]

    This will make sure that title remains unique while creating the menuitem
    title = serializers.CharField(max_length=255,
            validators=[UniqueValidator(queryset=MenuItem.objects.all())])

    """
    stock = serializers.IntegerField(source='inventory')
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, min_value=2)
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # category = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    # title = serializers.CharField(max_length=255, validators=[UniqueValidator(queryset=MenuItem.objects.all())])
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']
        validators = [
            UniqueTogetherValidator(
                queryset=MenuItem.objects.all(),
                fields=['title', 'price']
            ),
        ]
        extra_kwargs = {
            'price': {'min_value': 2},
            'stock': {'min_value': 0},
            # 'title': {
            #     'validators': [
            #         UniqueValidator(
            #             queryset=MenuItem.objects.all()
            #         )
            #     ]
            # }
        }

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)

    # def validate_price(self, value):
    #     if (value < 2):
    #         raise serializers.ValidationError('Price should not be less than 2.0')
    #
    # def validate_stock(self, value):
    #     if (value < 0):
    #         raise serializers.ValidationError('Stock cannot be negative')

    def validate(self, attrs):
        if (attrs['price'] < 2):
            raise serializers.ValidationError('Price should not be less than 2.0')
        if (attrs['inventory'] < 0):
            raise serializers.ValidationError('Stock cannot be negative')
        return super().validate(attrs)


class MenuItemSerializer1(serializers.ModelSerializer):
    """
    Serializer example for depth which will show the data within the category since
    we pass depth = 1
    """

    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')

    # category = CategorySerializer()

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category']
        depth = 1

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)


class MenuItemSerializer2(serializers.ModelSerializer):
    """
    Serializer example for HyperlinkedRelatedField
    """
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    category = serializers.HyperlinkedRelatedField(queryset=Category.objects.all(), view_name='category-detail')

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category']

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)
