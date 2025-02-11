from django.db import models
from django.core.validators import MinValueValidator as mini
from accounts.models import accounts 




# Create your models here.





class shop(models.Model):
    shop_owner = models.ForeignKey(to = accounts , on_delete=models.CASCADE , related_name='account_in_shop')
    shop_name = models.CharField(max_length= 200    ,   verbose_name= 'shop_name'    )
    address = models.CharField(max_length= 300    ,   verbose_name= 'address'    )
    email   = models.EmailField(   verbose_name= 'shop_email'    )
    footer_brief_slogan = models.CharField(max_length=  200   ,   verbose_name=   'shop_footer_brief_slogan'  )
    footer_slogan = models.CharField(max_length=  400   ,   verbose_name=   'footer_slogan'  )
    footer_slogan_description = models.TextField(max_length= 500    ,   verbose_name= 'footer_slogan_descrition'    )

    def __str__(self) -> str:
        return f'{self.id} : shop : {self.shop_name} - {self.shop_owner.user.username} - {self.shop_owner.phone_number} '





class home_pages(models.Model):
    owner = models.ForeignKey(to=accounts , on_delete=models.CASCADE , related_name='account_in_home_page')

    slogan_number = models.IntegerField(  verbose_name='home_slogan_number' , default =  2041    )
    slogan_part = models.CharField(max_length=100 , verbose_name='home_slogan') 

    goal_number = models.IntegerField(  verbose_name='home_slogan_number' , default =  2042    )
    goal_part = models.CharField(max_length=100 , verbose_name='home_slogan') 




class feature_table(models.Model):
    name = models.CharField(max_length=50 , verbose_name='نام ویژگی') 
    amount = models.CharField(max_length=50 , verbose_name='میزان یا تعداد ویژگی' )


class product(models.Model):
    name = models.CharField(max_length=200 , verbose_name='نام محصول') 
    tag = models.CharField(max_length=200 , verbose_name='دسته بندی') 
    price  = models.IntegerField( verbose_name='قیمت' , validators=[mini(0)] )
    picture = models.ImageField(blank=True , null=True , verbose_name='عکس محصول')
    description = models.TextField(blank=True , null=True , verbose_name='توضیحات')
    features =  models.ManyToManyField(feature_table , verbose_name='ویژگی ها')
    def __str__(self) :
        return f'{self.id} <-> {self.name}'


class messages(models.Model):
    name = models.CharField(max_length=100   , verbose_name='نام' )
    email  = models.EmailField(verbose_name='ایمیل') 
    message = models.TextField(max_length=400 , verbose_name='پیام')

