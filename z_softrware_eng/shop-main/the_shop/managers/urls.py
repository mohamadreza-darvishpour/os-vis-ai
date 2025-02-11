from django.contrib import admin
from django.urls import path 
from . import views



#needed parts : 1-dashboard   2-transacttions   3-carts   4-specific_clientbase_page   5-specific_cart_basepage 6-clients  7-carts  8-products 9-specific_product

urlpatterns = [
    path('dashboard/', views.dashboard.as_view() , name ='dashboard'),
    path('add_product/', views.test.as_view() , name ='add_product'),
    path('products/', views.test.as_view() , name ='products'),
    path('specific_product/', views.test.as_view() , name ='specific_product'),
    path('transactions/', views.test.as_view() , name ='transactions'),
    path('carts/', views.test.as_view() , name ='carts'),
    path('specific_client/', views.test.as_view() , name ='specific_client'),
    path('specific_cart/', views.test.as_view() , name ='specific_cart'),
    path('client/', views.test.as_view() , name ='client'),
    # path('manage_products/', views.manage_products.as_view() , name ='manage_products'),

]



