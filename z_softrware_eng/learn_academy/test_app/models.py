from django.db import models
from django.contrib.auth.models import User


class categories(models.Model):
    title = models.CharField(max_length=200, verbose_name='نام')
    number = models.IntegerField(verbose_name='تعداد')  
    picture = models.ImageField(upload_to='category_pic' ,verbose_name='عکس دسته بندی')

class Course(models.Model):
    title = models.CharField(null=True , blank=True ,max_length=200)
    description = models.TextField(null=True , blank=True ,)
    duration = models.CharField(null=True , blank=True , max_length=50)  # Example: "10 weeks"
    price = models.IntegerField(null=True , blank=True , verbose_name='price'    )
    students_number = models.IntegerField(null=True , blank=True , verbose_name='students_number'    )   
    lecturer = models.CharField(null=True , blank=True , max_length=100,verbose_name='lecturer')
    stars = models.IntegerField(null=True , blank=True ,default=4 , verbose_name='stars')
    picture = models.ImageField(upload_to='course_item' , null=True , blank=True )
    def __str__(self):
        return self.title

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    photo = models.ImageField(upload_to='team_photos/', blank=True, null=True)

    def __str__(self):
        return self.name

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    message = models.TextField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.date}"