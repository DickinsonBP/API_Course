from rest_framework import serializers
from .models import *
from decimal import Decimal

from datetime import datetime


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','slug','title']
        
class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    class Meta:
        model = MenuItem
        fields = ['id','title','price','featured','category','category_id']

class UserSerializer(serializers.ModelSerializer):
    Date_Joined = serializers.SerializerMethodField()
    date_joined = serializers.DateTimeField(write_only=True, default=datetime.now)
    email = serializers.EmailField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'Date_Joined']

    def get_Date_Joined(self, obj):
        return obj.date_joined.strftime('%Y-%m-%d')

class CartSerializer(serializers.ModelSerializer):
    unit_price = serializers.DecimalField(max_digits=6, decimal_places=2, source='menuitem.price', read_only=True)
    name = serializers.CharField(source='menuitem.title', read_only=True)
    total_price = serializers.SerializerMethodField(method_name = 'calculate_total_price')
    class Meta:
        model = Cart
        fields = ['user_id', 'menuitem', 'name', 'quantity', 'unit_price', 'price', 'total_price']
        extra_kwargs = {
            'price': {'read_only': True}
        }
    
    def calculate_total_price(self, cart_items:Cart):
        return cart_items.price
        
