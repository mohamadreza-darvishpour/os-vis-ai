from django.contrib import admin
from django.urls import path 
from . import views

urlpatterns = [
    path('index/',  views.index.as_view() , name='index'),
    path('contact/',  views.contact.as_view() , name='contact'),
    path('courses/',  views.courses.as_view() , name='courses'),
    
]









