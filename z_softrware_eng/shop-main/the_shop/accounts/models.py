from django.db import models
from django.contrib.auth import get_user_model 
from django.core.validators import MaxValueValidator as maxv 
from django.core.validators import MinValueValidator as minv 
def_user = get_user_model()

# Create your models here.



class accounts(models.Model) :
    user = models.ForeignKey(def_user , on_delete=models.CASCADE , related_name='user_account')
    profile_picture = models.ImageField( blank=True, null=True , verbose_name='profile_picture')
    phone_number = models.IntegerField( verbose_name='phone_number' , validators=[maxv(9999999999) , minv(1000000000)])


    def __str__(self): 
        return f'{self.user.username} <-> {self.phone_number}'












