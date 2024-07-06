from rest_framework import serializers
from LittleLemonAPI.models import *
from decimal import Decimal


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'slug', 'title']


class MenuItemSerializer(serializers.ModelSerializer):
    """
    read_only=True
    won't be used in post request. will only be used for displaying
    """
    stock = serializers.IntegerField(source='inventory')
    price_after_tax = serializers.SerializerMethodField(method_name='calculate_tax')
    # category = serializers.StringRelatedField()
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'stock', 'price_after_tax', 'category', 'category_id']

    def calculate_tax(self, product: MenuItem):
        return product.price * Decimal(1.1)


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
