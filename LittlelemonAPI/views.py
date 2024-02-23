from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import User, Group

from rest_framework.response import Response
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

from .models import *
from .serializers import *
# Create your views here.

# The `CategoryListView` class in Python defines a view for listing and creating Category objects,
# with a check to ensure only admin users can add a new category.
class CategoryListView(ListCreateAPIView):
    queryset = Category.objects.all().order_by('id')
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdminUser()]
        return [AllowAny()]

class SingleCategoryView(RetrieveAPIView, RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'PUT' \
                or self.request.method == 'DELETE' or self.request.method == 'PATCH':
            return [IsAdminUser()]
        return [AllowAny()]

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
        return [AllowAny()]
    
class SingleMenuItemView(RetrieveAPIView, RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer
    def get_permissions(self):
        if self.request.method == 'POST' or self.request.method == 'PUT' \
                or self.request.method == 'DELETE' or self.request.method == 'PATCH':
            return [IsAdminUser()]
        return [AllowAny()]
    
"""
This Python function allows an system admin user to add or remove a specified user from the 'Manager'
group.

:param request: The `request` parameter in the code snippet represents the HTTP request object that
Django receives when a client makes a request to the API endpoint. It contains information about the
request, such as the method (POST, DELETE), data sent in the request body, headers, user
authentication details, and more
:return: The code snippet provided is a Django REST framework view function for managing users in
the "Manager" group.
"""
@api_view(['POST', 'DELETE'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Manager')
            
        if request.method == 'POST':
            managers.user_set.add(user)
            message = f"User {username} added to manager group"
            
        if request.method == 'DELETE':
            managers.user_set.remove(user)
            message = f"User {username} deleted from manager group"
            
        return Response({"message":message})
    
    return Response({"message":"error"}, status.HTTP_400_BAD_REQUEST)

"""
This function allows an admin user to add or remove a user from the 'Manager' group based on a POST
or DELETE request.

:param request: The code you provided is a Django REST framework view function for managing delivery
crew members. It allows adding or removing a user from the 'Manager' group based on the request
method (POST or DELETE)
:return: The code snippet defines a Django REST framework view function for managing delivery crew
members. The function accepts POST and DELETE requests and requires the user to be an admin user.
"""
@api_view(['POST', 'DELETE'])
@permission_classes([IsAdminUser])
def delivery_crew(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Delivery Crew')
            
        if request.method == 'POST':
            managers.user_set.add(user)
            message = f"User {username} added to delivery crew group"
            
        if request.method == 'DELETE':
            managers.user_set.remove(user)
            message = f"User {username} deleted from delivery crew group"
            
        return Response({"message":message})
    
    return Response({"message":"error"}, status.HTTP_400_BAD_REQUEST)


class CartView(APIView):
    def get(self, request):
        cart_items = Cart.objects.all()
        serializer = CartSerializer(cart_items, many=True)
        return Response(serializer.data)
    def post(self, request):
        return Response({"message":"HOLA"})
    def delete(self, request):
        return Response({"message":"HOLA"})