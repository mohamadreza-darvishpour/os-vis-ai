from django import forms 
from . import models 




class course_filter(forms.ModelForm):
    class Meta :
        model = models.course
        fields = ['price' ]





