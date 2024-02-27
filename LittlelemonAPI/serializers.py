from rest_framework import serializers
from .models import *
from decimal import Decimal

from datetime import datetime


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']
        
class MenuItemSerializer(serializers.ModelSerializer):
    # category = CategorySerializer(read_only=True)
    # category_id = serializers.IntegerField(write_only=True)
    category = serializers.PrimaryKeyRelatedField(
        queryset = Category.objects.all()
    )
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username','email']

class CartSerializer(serializers.ModelSerializer):
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='menuitem.price', read_only=True)
    name = serializers.CharField(source='menuitem.title', read_only=True)
    class Meta:
        model = Cart
        fields = ['user_id', 'menuitem', 'name', 'quantity', 'unit_price', 'price']
        extra_kwargs = {
            'price': {'read_only': True}
        }


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['order', 'menuitem', 'quantity', 'price']


class OrderSerializer(serializers.ModelSerializer):
    orderitem = OrderItemSerializer(many=True, read_only=True, source='order')

    class Meta:
        model = Order
        fields = ['id', 'user', 'delivery_crew',
                  'status', 'date', 'total', 'orderitem']

