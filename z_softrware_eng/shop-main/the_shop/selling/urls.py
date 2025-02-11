
from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('index/', views.index.as_view() , name ='index'),
    path('shop/', views.shop.as_view() , name ='shop'),
    path('contact/', views.contact.as_view() , name ='contact'),
    path('about/', views.about.as_view() , name ='about'),
    path('detail/', views.product_detail.as_view() , name ='detail'),
    path('prod/<slug:product_slug>', views.specific_product.as_view() , name ='specific-prod'),
    path('', views.shop.as_view() , name ='empty_shop'),
]




