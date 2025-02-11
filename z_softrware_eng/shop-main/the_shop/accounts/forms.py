from django.forms import ModelForm 
from django import forms
from django.contrib.auth import get_user_model 
user = get_user_model()

from . import models

class username_form(ModelForm):
    class Meta:
        model = user
        fields = ['username'] 


class signin_form(forms.Form):
    username = forms.CharField(max_length=100 ,required=True  ,
        widget=forms.TextInput(attrs={
            # 'id': 'custom-id',
            'class': 'form-control',
            'placeholder': 'Username'
        }) )
    
    password = forms.CharField( widget=forms.TextInput(attrs={
            'id': 'password-field',
            'type': 'password',
            'class': 'form-control',
            'placeholder': 'Password'
        }))

class signup_form(forms.Form):
    username = forms.CharField(max_length=100 ,required=True  ,
        widget=forms.TextInput(attrs={
            # 'id': 'custom-id',
            'class': 'form-control',
            'placeholder': 'Username'
        }) )
    

    email = forms.EmailField(widget=forms.TextInput(attrs={
            # 'id': 'custom-id',
            'class': 'form-control',
            'placeholder': 'Email'
        }))


    phone = forms.IntegerField(widget=forms.NumberInput(attrs={
            # 'id': 'custom-id',
            'class': 'form-control',
            'placeholder': 'phone'
        }))

    password = forms.CharField( widget=forms.TextInput(attrs={
            'id': 'password',
            'class': 'form-control',
            'type': 'password-field',
            'placeholder': 'Password'
        }))
    confirm_password = forms.CharField( widget=forms.TextInput(attrs={
            'id': 'password-field',
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'Confirm Password'
        }))