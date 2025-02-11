from django import forms    
from . import models 




class message_form(forms.ModelForm):

    class Meta:
        model = models.messages    
        fields = '__all__' 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control border-0 me-4', 'placeholder': 'نام '}),
            'email': forms.EmailInput(attrs={'class': 'form-control border-0', 'placeholder': 'ایمیل'}),
            'message': forms.Textarea(attrs={'rows': 3 ,'class': 'form-control border-0', 'placeholder': 'پیام'}),
        }


class message_in_contact(forms.ModelForm):

    class Meta:
        model = models.messages    
        fields = '__all__' 
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-100 form-control border-0 py-3 mb-4', 'placeholder': 'نام '}),
            'email': forms.EmailInput(attrs={'class': 'w-100 form-control border-0 py-3 mb-4', 'placeholder': 'ایمیل'}),
            'message': forms.Textarea(attrs={'rows': 3 ,'class': 'w-100 form-control border-0 mb-4', 'placeholder': 'پیام'}),
        }


