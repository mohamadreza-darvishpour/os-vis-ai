from django.shortcuts import render
from django import views
from . import models
# Create your views here.



class  index(views.View):
    def get(self , request):


       return render(request , 'test_app/index.html')  



    def post(self , request):
        

        return render(request , 'test_app/index.html')






class  courses(views.View):
    def get(self , request):
        datas = {}
        course_obj = models.course.objects.all()
        datas['courses'] = course_obj

        return render(request , 'test_app/courses.html' , datas )  



    def post(self , request):


        return render(request , 'test_app/courses.html')






class  contact(views.View):
    def get(self , request):


       return render(request , 'test_app/contact.html')  



    def post(self , request):
        

        return render(request , 'test_app/courses.html')






