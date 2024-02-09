from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view
from rest_framework.views import APIView

from .models import MenuItem
from .serializers import MenuItemSerializer

# Create your views here.
#ListCreateAPIView can display records and accept POST calls to create a new record
# The MenuItemView class is a generic view that allows for listing and creating MenuItem objects,
# using the MenuItemSerializer for proper serialization.
class MenuItemView(generics.ListCreateAPIView):
    queryset = MenuItem.objects.all()   #retrive all the records using a model
    serializer_class = MenuItemSerializer   #serializer class to display and store the records properly


# The SingleMenuItemView class is a generic view that allows for retrieving, updating, and deleting a
# single MenuItem object.
class SingleMenuItemView(generics.RetrieveUpdateAPIView, generics.DestroyAPIView):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer