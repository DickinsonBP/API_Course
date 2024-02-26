from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User, Group

from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .models import *
from .serializers import *
# Create your views here.

class IsAdminOrManager(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        
        manager_group = Group.objects.get(name='Manager')
        if manager_group in request.user.groups.all():
            return True
        
        return False

# The `CategoryListView` class in Python defines a view for listing and creating Category objects,
# with a check to ensure only admin users can add a new category.
class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer
    # permission_classes = [IsAdminUser]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [IsAuthenticated()]

class SingleCategoryView(RetrieveAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'PUT' \
                or self.request.method == 'DELETE' or self.request.method == 'PATCH':
            return [IsAdminUser()]
        return [IsAuthenticated()]

# The `MenuItemListView` class extends `ListCreateAPIView` to handle GET and POST requests for menu
# items, with a custom permission check for admin users before allowing item creation.

class MenuItemView(ListAPIView, ListCreateAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    ordering_fields = ['price']
    search_fields = ['title']
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        if self.request.method == 'PATCH':
            return [IsAdminOrManager()]
        return [IsAuthenticated()]
    
class SingleMenuItemView(RetrieveAPIView, RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'PUT' \
                or self.request.method == 'DELETE' or self.request.method == 'PATCH':
            return [IsAdminUser()]
        return [IsAuthenticated()]


# The `ManagerUsersView` class is a Django API view that lists and creates users who belong to the
# 'Manager' group.
class ManagerUsersView(ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
    
    def get_queryset(self):
        managers = Group.objects.get(name='Manager')
        return User.objects.filter(groups=managers)
    
    def perform_create(self, serializer):
        managers = Group.objects.get(name='Manager')
        user = serializer.save()
        user.groups.add(managers)

# This class is a Django REST framework view for managing users belonging to the "Delivery Crew"
# group.
class DeliveryCrewUsersView(ListCreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrManager]
    
    def get_queryset(self):
        delivery_crew = Group.objects.get(name='Delivery Crew')
        return User.objects.filter(groups=delivery_crew)
    
    def perform_create(self, serializer):
        delivery_crew = Group.objects.get(name='Delivery Crew')
        user = serializer.save()
        user.groups.add(delivery_crew)

class CartView(ListCreateAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(user=user)

    def perform_create(self, serializer):
        menuitem_id = self.request.data.get('menuitem')
        quantity = self.request.data.get('quantity')
        unit_price = MenuItem.objects.get(pk=menuitem_id).price
        quantity = int(quantity)
        price = quantity * unit_price
        serializer.save(user=self.request.user, price=price, unit_price=unit_price)

    def delete(self, request):
        user = self.request.user
        Cart.objects.filter(user=user).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class OrderView(ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        return Order.objects.filter(user=user)

class SingleOrderView(RetrieveAPIView, RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name='Manager').exists():
            return Order.objects.all()
        return Order.objects.filter(user=user)