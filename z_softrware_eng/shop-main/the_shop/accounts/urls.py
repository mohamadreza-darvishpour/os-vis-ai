
from django.contrib import admin 
from django.urls import path 
from . import views

urlpatterns = [
        path('profile-<str:username>/', views.profile.as_view() , name= 'profile_id'),  
        path('profile/', views.profile.as_view() , name= 'profile'),  
        path('registeration/', views.registeration.as_view() , name= 'registration'),  
        path('registeration--<str:reg_type>/', views.registeration.as_view() , name= 'registration2'),  
]




