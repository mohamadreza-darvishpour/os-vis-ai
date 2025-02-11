from django.shortcuts import render
from django import views
from selling import models as sell_model
# Create your views here.



class dashboard(views.View):
    def get(self , request):
        datas = {} 
        features = sell_model.feature_table.objects.all()
        print('\n\n\n\n******\n' , features , '\\n\n\n\n')
        datas['cards'] = features

        return render(request , 'managers/index.html' , datas)



    def post(self , request):
        pass
















class test(views.View):
    def get(self , request):
        pass 

    def post(self , request):
        pass 


    