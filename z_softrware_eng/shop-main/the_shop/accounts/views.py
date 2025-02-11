from django.shortcuts import render , redirect 
from django.urls import reverse 
from django.contrib.auth import login , logout 
from django import views
from . import forms , models
from django.contrib.auth import get_user_model 
user_model = get_user_model()
# Create your views here.


class profile(views.View):
    def get(self , request , username=None):
        form = forms.username_form()
        try:
            # user_name = request.GET.get('username')   #not work maybe not use 
            #default rule of url parameters. like ? < and ...
            user_name = username
            print('\n\nusername got from get : ',user_name)
        except:
            user_name = None
            pass
        datas = {'form' : form ,
                 'username' : None ,
                 'profile_picture' : None , 
                 } 
        print('\n\n******\n',username)
        user = user_model.objects.all().filter(username=user_name).first() 
        if user:
            print('\npic : \n',user)
            account = models.accounts.objects.all().filter(user=user).first()
            # account = user.user_account 
            datas['profile_picture'] = account.profile_picture
            print("\n\n******\n",account.profile_picture)


        return render(request , 'accounts/profile.html' , datas ) 
    
    def post(self , request , *args , **kwargs):
        form = forms.username_form(request.POST)
        datas = {'form' : form ,} 
        user_name = request.POST.get('username')
        #below validation check existance of username auto. not need. 
        # if not form.is_valid():
        #     form.errors["not_valid" ] = 'validation error.'
        # form.add_error(None, 'Validation failed. Please check your input.')    #better to use
        #     return render(request , 'accounts/profile.html' , datas ) 
        # if user_model.objects.all().filter(username=form.cleaned_data['username']).first() :
        
        
         
        if user_model.objects.all().filter(username=user_name).first() : 
            return redirect(reverse('index') , username='')
        else:
            form.errors['not_found'] = '<<could not found the username.>>'
        
        return render(request , 'accounts/profile.html' , datas ) 
    





class registeration(views.View):
    def get(self , request , reg_type = None):
        datas={
            "status" : 'no_status'
        }
        if (reg_type == None ):
            cur_form = forms.signin_form()
        elif(reg_type=='sign-up'):
            cur_form = forms.signup_form() 


        datas['form'] = cur_form 

        return render(request , 'accounts/login.html' , datas )



    def post(self , request , reg_type = 'sign-in'):
        datas = {'status' : "no_status"}
        if (reg_type == None ):
            cur_form = forms.signin_form()

        elif(reg_type=='sign-in'):
            cur_form = forms.signin_form(request.POST)
            if not cur_form.is_valid():
                cur_form.errors['validation_error'] = 'error in validation. '
            username , password = cur_form.cleaned_data['username'], cur_form.cleaned_data['password']
            user = user_model.objects.all().filter(username=username).first()
            if(user.check_password(password)):
                login(request , user = user)
                # logout(request) 
                datas['status'] = 'login'


        elif(reg_type=='sign-up'):
            cur_form = forms.signup_form() 

        return render( request , 'accounts/login.html' , datas)
    



















