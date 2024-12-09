from django.db import models

# Create your models here.



class course(models.Model ):
    teacher = models.CharField(max_length=100) 
    price = models.IntegerField(verbose_name='price' ) 
    description = models.TextField() 
    image = models.ImageField(upload_to='course_image')




