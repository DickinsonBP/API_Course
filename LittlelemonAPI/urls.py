from django.urls import path
from . import views

from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # path('menu-items', views.MenuItemView.as_view()),
    path('menu-items/', views.menu_items),
    # path('menu-items/<int:pk>', views.SingleMenuItemView.as_view()),
    path('menu-items/<int:id>', views.single_item),
    path('secret/', views.secret),
    path('manager-view/', views.manager_view),
    path('api-token-auth/', obtain_auth_token),
]
