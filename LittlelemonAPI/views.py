from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator, EmptyPage
from django.contrib.auth.models import User, Group

from rest_framework.response import Response
from rest_framework import status, viewsets, generics
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle


from .models import MenuItem
from .serializers import MenuItemSerializer
from .throttles import TenCallsPerMinute

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
    
@api_view(['GET','POST'])
def menu_items(request):
    if(request.method == 'GET'):
        items = MenuItem.objects.select_related('category').all()
        category_name = request.query_params.get('category')
        to_price = request.query_params.get('to_price')
        search = request.query_params.get('search')
        ordering = request.query_params.get('ordering')
        
        perpage = request.query_params.get('perpage',default=2)
        page = request.query_params.get('ordering',default=1)
        
        
        # filtrado
        if category_name:
            items = items.filter(category__title=category_name)
        if to_price:
            items = items.filter(price=to_price)
        
        #busqueda
        if search:
            items = items.filter(title__startswith=search)
        
        # ordenado
        if ordering:
            ordering_fields = ordering.split(",")
            items = items.order_by(*ordering_fields)
        
        # paginacion
        paginator = Paginator(items, per_page=perpage)
        
        try:
            items = paginator.page(number=page)
        except EmptyPage:
            items = []      # pagina vacía
            
        serlized_item = MenuItemSerializer(items, many=True)
        return Response(serlized_item.data)
    
    if(request.method == 'POST'):
        serlized_item = MenuItemSerializer(data=request.data)
        serlized_item.is_valid(raise_exception=True) #comprobar que todos los campos son correctos, si falta alguno, mostrar error.
        serlized_item.save()
        return Response(serlized_item.data, status.HTTP_201_CREATED)

@api_view()
def single_item(request, id):
    item = get_object_or_404(MenuItem, pk=id)
    serlized_item = MenuItemSerializer(item)
    return Response(serlized_item.data)

@api_view()
@permission_classes([IsAuthenticated])
def secret(request):
    return Response({"message":"Some secret message"})

@api_view()
@permission_classes([IsAuthenticated])
def manager_view(request):
    if request.user.groups.filter(name='Manager').exists():
        return Response({"message":"Only Manager Should See This"})
    else:
        return Response({"message":"You are not authorized"}, 403)
    
    
@api_view()
@throttle_classes([AnonRateThrottle])
def throttle_check(request):
    return Response({"message":"successful"})

@api_view()
@permission_classes([IsAuthenticated])
@throttle_classes([TenCallsPerMinute])
def throttle_check_auth(request):
    return Response({"message":"message for the logged in users only"})


@api_view(['POST, DELETE'])
@permission_classes([IsAdminUser])
def managers(request):
    username = request.data['username']
    if username:
        user = get_object_or_404(User, username=username)
        managers = Group.objects.get(name='Manager')
        if request.method == 'POST':
            managers.user_set.add(user)
            
        if request.method == 'DELETE':
            managers.user_set.remove(user)
            
        return Response({"message":"ok"})
    return Response({"message":"error"}, status.HTTP_400_BAD_REQUEST)