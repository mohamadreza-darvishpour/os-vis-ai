from django.shortcuts import render
from django import views
from . import models , forms
# Create your views here.



class  index(views.View):
    def get(self , request):


       return render(request , 'test_app/index.html')  



    def post(self , request):
        

        return render(request , 'test_app/index.html')






class  courses(views.View):
    def get(self , request):
        course_filter = forms.course_filter()
        datas = {}
        course_obj = models.course.objects.all()
        datas['courses'] = course_obj
        datas['price_filter'] = course_filter

        return render(request , 'test_app/courses.html' , datas )  



    def post(self , request):

        course_filter = forms.course_filter(request.POST)
        datas = {}
        datas['price_filter'] = course_filter
        if(course_filter.is_valid()):
            price = course_filter.cleaned_data['price']
            course_obj = models.course.objects.filter(price=price)
        else :
            course_obj = models.course.objects.all()
        datas['courses'] = course_obj
        return render(request , 'test_app/courses.html' , datas )  






class  contact(views.View):
    def get(self , request):


       return render(request , 'test_app/contact.html')  



    def post(self , request):
        

        return render(request , 'test_app/courses.html')






