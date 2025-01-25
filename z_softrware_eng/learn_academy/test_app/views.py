from django.shortcuts import render
from django.views import View
from .models import Course, TeamMember, Testimonial
from .forms import ContactForm, TestimonialForm
from . import models

class IndexView(View):
    def get(self, request):
        categories = models.categories.objects.all()
        courses = models.Course.objects.all()
        
        datas = {
            'categories' : categories ,
            'courses': courses , 
        }
        return render(request, 'test_app/index.html', datas)

class AboutView(View):
    def get(self, request):
        return render(request, 'test_app/about.html')

class ContactView(View):
    def get(self, request):
        form = ContactForm()
        return render(request, 'test_app/contact.html', {'form': form})

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            # Handle the form data (e.g., send email)
            return render(request, 'test_app/contact.html', {'form': form, 'success': True})
        return render(request, 'test_app/contact.html', {'form': form})

class CoursesView(View):
    def get(self, request):
        courses = Course.objects.all()
        return render(request, 'test_app/courses.html', {'courses': courses})

class TeamView(View):
    def get(self, request):
        team_members = TeamMember.objects.all()
        return render(request, 'test_app/team.html', {'team_members': team_members})

class TestimonialView(View):
    def get(self, request):
        testimonials = Testimonial.objects.all()
        form = TestimonialForm()
        return render(request, 'test_app/testimonial.html', {'testimonials': testimonials, 'form': form})

    def post(self, request):
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'test_app/testimonial.html', {'form': form, 'success': True})
        testimonials = Testimonial.objects.all()
        return render(request, 'test_app/testimonial.html', {'testimonials': testimonials, 'form': form})

class NotFoundView(View):
    def get(self, request):
        return render(request, 'test_app/404.html')
