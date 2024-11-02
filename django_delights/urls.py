"""
URL configuration for django_delights project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from inventory_sales import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.home, name='home'),
    path('add-ingredient/', views.add_ingredient, name='add_ingredient'),
    path('add-menu-item/', views.add_menu_item, name='add_menu_item'),
    path('record-purchase/', views.record_purchase, name='record_purchase'),
    path('login/', views.user_login, name='login'),
    path('signup/', views.user_signup, name='signup'),
    path('logout/', views.user_logout, name='logout'),
    path('menu-items/', views.menu_item_list, name='menu_item_list'),
    path('ingredients/', views.ingredient_list, name='ingredient_list'),
    path('purchase-history/', views.purchase_history, name='purchase_history'),
]
