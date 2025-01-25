from django.urls import path
from .views import (
    AboutView, ContactView, CoursesView, IndexView, TeamView, TestimonialView, NotFoundView
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('courses/', CoursesView.as_view(), name='courses'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('team/', TeamView.as_view(), name='team'),
    path('testimonial/', TestimonialView.as_view(), name='testimonial'),
    path('404/', NotFoundView.as_view(), name='404'),
]