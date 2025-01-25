from django.shortcuts import render
from django.views import View
from .models import Course, TeamMember, Testimonial
from .forms import ContactForm, TestimonialForm
from . import models

class IndexView(View):
    def get(self, request):
    
        categories = models.categories.objects.all()
        courses = models.Course.objects.all()
        lecturer = models.lecturer.objects.all()
        messages = models.message.objects.all()
        
        datas = {
            'page_name' : 'index',
            'categories' : categories ,
            'courses': courses , 
            'lecturers' : lecturer ,
            'messages' : messages   ,
        }
        return render(request, 'test_app/index.html', datas)

class AboutView(View):
    def get(self, request):
        categories = models.categories.objects.all()
        courses = models.Course.objects.all()
        lecturer = models.lecturer.objects.all()
        messages = models.message.objects.all()
        datas = {
            'page_name' : 'about',
            'categories' : categories ,
            'courses': courses , 
            'lecturers' : lecturer ,
            'messages' : messages   ,
        }
        return render(request, 'test_app/about.html' , datas)

from . import forms
class ContactView(View):
    def get(self, request):
        form = forms.ContactForm()
        categories = models.categories.objects.all()
        courses = models.Course.objects.all()
        lecturer = models.lecturer.objects.all()
        messages = models.message.objects.all()
        datas = {
            'page_name' : 'contact',
            'categories' : categories ,
            'courses': courses , 
            'lecturers' : lecturer ,
            'messages' : messages   ,
            'form'  : form , 
        }
        return render(request, 'test_app/contact.html', datas)

    def post(self, request):
        form = ContactForm(request.POST)
        if form.is_valid():
            # Handle the form data (e.g., send email)
            return render(request, 'test_app/contact.html', {'form': form, 'success': True})
        return render(request, 'test_app/contact.html', {'form': form})

class CoursesView(View):
    def get(self, request):
        categories = models.categories.objects.all()
        courses = models.Course.objects.all()
        lecturer = models.lecturer.objects.all()
        messages = models.message.objects.all()
        datas = {
            'page_name' : 'courses',
            'categories' : categories ,
            'courses': courses , 
            'lecturers' : lecturer ,
            'messages' : messages   ,
        }
        return render(request, 'test_app/courses.html', datas)

class TeamView(View):
    def get(self, request):
        categories = models.categories.objects.all()
        courses = models.Course.objects.all()
        lecturer = models.lecturer.objects.all()
        messages = models.message.objects.all()
        datas = {
            'page_name' : 'team',
            'categories' : categories ,
            'courses': courses , 
            'lecturers' : lecturer ,
            'messages' : messages   ,
        }
        return render(request, 'test_app/team.html', datas)

class TestimonialView(View):
    def get(self, request):
        categories = models.categories.objects.all()
        courses = models.Course.objects.all()
        lecturer = models.lecturer.objects.all()
        messages = models.message.objects.all()
        datas = {
            'page_name' : 'testimonial',
            'categories' : categories ,
            'courses': courses , 
            'lecturers' : lecturer ,
            'messages' : messages   ,
        }
        return render(request, 'test_app/testimonial.html',datas)

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
