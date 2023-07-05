"""
URL configuration for xelashop project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from xelashopapp.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('men/', men_product, name='men'),
    path('women/', women_product, name="women"),
    path('men/search/', search, name="search"),
    path('women/search/', search_women, name="search_women"),
    path('men_product_details/<int:product_id>/', men_product_details, name="men_product_details"),
    path('women_product_details/<int:product_id>/', women_product_details, name="women_product_details"),
    path('checkout/', checkout, name='checkout'),
    path('final_site/', final_site, name="final_site"),
    path('item/delete/<int:item_id>/', delete_item, name='delete_item'),
    path('process_order/', process_order, name='process_order'),
    path('add_to_bag/<int:product_id>/', add_to_bag, name='add_to_bag'),
    path('item/delete/<int:item_id>/', delete_item, name='delete_item'),
    path('cart/item/delete/<int:item_id>/', delete_cart_item, name='delete_cart_item'),
    path('order_confirmation/<int:order_id>/', order_confirmation, name='order_confirmation'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
