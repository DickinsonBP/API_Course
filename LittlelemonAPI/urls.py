from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('categories', views.CategoryListView.as_view()),
    path('categories/<int:pk>', views.SingleCategoryView.as_view()),
    path('cart', views.CartView.as_view()),
    path('api-token-auth', obtain_auth_token),
    path('groups/manager/users', views.managers),
    path('groups/delivery-crew/users', views.delivery_crew),
]