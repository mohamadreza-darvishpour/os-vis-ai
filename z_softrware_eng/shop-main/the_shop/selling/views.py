from django.shortcuts import render
from django import views
from . import models , forms
from django.http import JsonResponse 
from django.middleware.csrf import get_token
# Create your views here.


class index(views.View):
    def get(self , request ):
        datas = {}
        shop = models.shop.objects.all().first()
        datas['shop'] = shop


        datas['shop_name'] = 'shop_name' 
        datas['address'] = 'the_address , shiraz ,...' 
        datas['email'] = 'the_email@test.com' 
        datas['home_slogan'] = 'Home_slogan' 
        datas['home_goal'] = 'Home_goal' 
        datas['footer_brief_slogan'] = 'footer_brief_slogan: new products'
        datas['footer_slogan'] = 'footer slogan: why people like us ? '
        datas['footer_slogan_description'] = ' becaouse we alsdfj asldfovajwfoeifasdlkf a;slkl \n\nldjsfa\nalsdkjf \n'


        datas['benefits'] = { 1 :{'Security Payment' : '100% security payment'} , 
                              2 : {'brief sent':'sentence'} , 
                              3 : {3 :'benef3'} , 
                              4 : {4 :'benef4'} , 
                              5 : {5 :'benef5'} ,} 
        
        datas['home_category_sentece'] = 'home_category_sentece' 
        datas['categories'] = ['all' , 'cat1' , 'cat2' ] 
        datas['prods_by_cat'] = {
                        'all' :{                    
                                    'name' :  'one' , 
                                    'description' : 'desc ..lab lb labbbbb' , 
                                    'price' : '93828.3 $' , 
                                    },
                        'cat1' :{
                                    'name' :  'one' , 
                                    'description' : 'desc ..lab lb labbbbb' , 
                                    'price' : '93828.3 $' , 
                                    },
                        'cat2' :{
                                    'name' :  'one' , 
                                    'description' : 'desc ..lab lb labbbbb' , 
                                    'price' : '93828.3 $' , 
                                    },

        }
        datas['home_first_picture'] = None 

        datas['home_features'] = {
                    1   :    {
                        'first_slogan' : 'first sent' , 
                        'second_slogan' :   'second sent' , 
                        'color_class'   :    'bg-primary',
                             } , 
                    2   :    {
                        'first_slogan' : 'first sent' , 
                        'second_slogan' :   'second sent' , 
                        'color_class'   :   'bg-secondary' ,
                             } , 
                    3   :    {
                        'first_slogan' : 'first sent' , 
                        'second_slogan' :   'second sent' , 
                        'color_class'   :    'bg-dark',
                             } , 
                    4   :    {
                        'first_slogan' : 'first sent' , 
                        'second_slogan' :   'second sent' , 
                        'color_class'   :    'bg-primary'
                          } ,
                    5   :    {
                        'first_slogan' : 'first sent' , 
                        'second_slogan' :   'second sent' , 
                        'color_class'   :    'bg-dark'
                          } ,
        }

        datas['home_prod_scrol'] = {
                        1 :{                    
                                    'name' :  'one' ,
                                    'tag'  :  'any tag' ,
                                    'description' : 'desc ..lab lb labbbbb' , 
                                    'price' : '93828.3 $' , 
                                    },
                        2 :{
                                    'name' :  '2' ,
                                    'tag'  :  'any tag' ,
                                    'description' : 'desc ..lab lb labbbbb' , 
                                    'price' : '93828.3 $' , 
                                    },
                        3 :{
                                    'name' :  '3' ,
                                    'tag'  :  'any tag' ,
                                    'description' : 'desc ..lab lb labbbbb' , 
                                    'price' : '93828.3 $' , 
                                    },
                        4 :{
                                    'name' :  '4' ,
                                    'tag'  :  'any tag' ,
                                    'description' : 'desc ..lab lb labbbbb' , 
                                    'price' : '93828.3 $' , 
                                    },
                        5 :{
                                    'name' :  '5' ,
                                    'tag'  :  'any tag' ,
                                    'description' : 'desc ..lab lb labbbbb' , 
                                    'price' : '93828.3 $' , 
                                    },
                        6 :{
                                    'name' :  '6' ,
                                    'tag'  :  'any tag' ,
                                    'description' : 'desc ..lab lb labbbbb' , 
                                    'price' : '93828.3 $' , 
                                    },
                        7 :{
                                    'name' :  '7' ,
                                    'tag'  :  'any tag' ,
                                    'description' : 'desc ..lab lb labbbbb' , 
                                    'price' : '93828.3 $' , 
                                    },

        }
    
        datas['home_banner'] = {
                                    'first' : 'first senten l....akdfl' , 
                                    'second' : 'second sentence aldkf  alds fla dll adlf la sdlf' , 
                                    'description' :  'desccripadsfiapdsfl  alsdk fa lsdf al dff lallllll lanalbballablablablab' ,
                                    'price'    : '832 $', 
                                    'amount'  : 28 , 
                                    'amount_name'  : 'meter' , 
                                    }
       
       
        datas['home_best_seller'] = {  1  : {    'name' : 'name senten l....akdfl' , 
                                                'second' : 'second sentence aldkf  alds fla dll adlf la sdlf' , 
                                                'description' :  'desccripadsfiapdsfl  alsdk fa lsdf al dff lallllll lanalbballablablablab' ,
                                                'price'    : '832 $', 
                                                'amount'  : 28 , 
                                                'amount_name'  : 'meter' , 
                                            },
                                        2  : {    'name' : 'name senten l....akdfl' , 
                                                'second' : 'second sentence aldkf  alds fla dll adlf la sdlf' , 
                                                'description' :  'desccripadsfiapdsfl  alsdk fa lsdf al dff lallllll lanalbballablablablab' ,
                                                'price'    : '832 $', 
                                                'amount'  : 28 , 
                                                'amount_name'  : 'meter' , 
                                            },
                                         3   : {    'name' : 'name senten l....akdfl' , 
                                                'second' : 'second sentence aldkf  alds fla dll adlf la sdlf' , 
                                                'description' :  'desccripadsfiapdsfl  alsdk fa lsdf al dff lallllll lanalbballablablablab' ,
                                                'price'    : '832 $', 
                                                'amount'  : 28 , 
                                                'amount_name'  : 'meter' , 
                                            },
                                         4   : {    'name' : 'name senten l....akdfl' , 
                                                'second' : 'second sentence aldkf  alds fla dll adlf la sdlf' , 
                                                'description' :  'desccripadsfiapdsfl  alsdk fa lsdf al dff lallllll lanalbballablablablab' ,
                                                'price'    : '832 $', 
                                                'amount'  : 28 , 
                                                'amount_name'  : 'meter' , 
                                            },
                                         5   : {    'name' : 'name senten l....akdfl' , 
                                                'second' : 'second sentence aldkf  alds fla dll adlf la sdlf' , 
                                                'description' :  'desccripadsfiapdsfl  alsdk fa lsdf al dff lallllll lanalbballablablablab' ,
                                                'price'    : '832 $', 
                                                'amount'  : 28 , 
                                                'amount_name'  : 'meter' , 
                                            },
                                         6   : {    'name' : 'name senten l....akdfl' , 
                                                'second' : 'second sentence aldkf  alds fla dll adlf la sdlf' , 
                                                'description' :  'desccripadsfiapdsfl  alsdk fa lsdf al dff lallllll lanalbballablablablab' ,
                                                'price'    : '832 $', 
                                                'amount'  : 28 , 
                                                'amount_name'  : 'meter' , 
                                            },
                                    }
       
       
       
        datas['home_best_seller_white'] = {  1  : {    'name' : 'name senten l....akdfl' , 
                                                'second' : 'second sentence aldkf  alds fla dll adlf la sdlf' , 
                                                'description' :  'desccripadsfiapdsfl  alsdk fa lsdf al dff lallllll lanalbballablablablab' ,
                                                'price'    : '832 $', 
                                                'amount'  : 28 , 
                                                'amount_name'  : 'meter' , 
                                            },
                                        2  : {    'name' : 'name senten l....akdfl' , 
                                                'second' : 'second sentence aldkf  alds fla dll adlf la sdlf' , 
                                                'description' :  'desccripadsfiapdsfl  alsdk fa lsdf al dff lallllll lanalbballablablablab' ,
                                                'price'    : '832 $', 
                                                'amount'  : 28 , 
                                                'amount_name'  : 'meter' , 
                                            },
                                         3   : {    'name' : 'name senten l....akdfl' , 
                                                'second' : 'second sentence aldkf  alds fla dll adlf la sdlf' , 
                                                'description' :  'desccripadsfiapdsfl  alsdk fa lsdf al dff lallllll lanalbballablablablab' ,
                                                'price'    : '832 $', 
                                                'amount'  : 28 , 
                                                'amount_name'  : 'meter' , 
                                            },
                                               }
       
        datas['seller_history'] = {
           1 : {
            'quality' : 'sell times ' , 
            'number'  : '190%'
           }  ,
           2 : {
            'quality' : 'sell times ' , 
            'number'  : '190%'
           }  ,
           3 : {
            'quality' : 'sell times ' , 
            'number'  : '190%'
           }  ,
           4 : {
            'quality' : 'sell times ' , 
            'number'  : '190%'
           }  ,
           5 : {
            'quality' : 'sell times ' , 
            'number'  : '190%'
           }  ,
                                    }
       
        
        datas['testimonial_subject'] = 'testimo_subj : our testimonial'
        datas['home_comments_title']  = 'home_comments_title : Our Client Saying!'
        datas['home_client_comments'] = { 
                                        1 : {
                                            'name' : 'client382' ,
                                            'comment' : ' this is test to commmenssttssldfkja;dfvi' , 
                                            'degree'  : 'intermediate'
                                        } , 
                                        2 : {
                                            'name' : 'client382' ,
                                            'comment' : ' this is test to commmenssttssldfkja;dfvi' , 
                                            'degree'  : 'intermediate'
                                        } , 
                                        3 : {
                                            'name' : 'client382' ,
                                            'comment' : ' this is test to commmenssttssldfkja;dfvi' , 
                                            'degree'  : 'intermediate'
                                        } , 
                                        4 : {
                                            'name' : 'client382' ,
                                            'comment' : ' this is test to commmenssttssldfkja;dfvi' , 
                                            'degree'  : 'intermediate'
                                        } , 

                                        }
        

        return render(request , 'selling/index.html' ,datas )
    




    def post(self, request):
        pass






class shop(views.View):
    def get(self , request ):
        csrf = get_token(request)
        datas = {} 
        
        prods = models.product.objects.all()[:4]
        datas['products'] = prods
        datas['csrf_token'] = csrf 


        return render(request , 'selling/shop.html'  , datas)
  
  
    def post(self, request):
        datas = {} 
        
        prods = models.product.objects.all()[:4]
        
        prod_json = [{
            'name'  : product.name , 
            'tag'   : product.tag , 
            'price' : product.price , 
            'description' : product.tag , 
        }   for product in prods ]
        datas['products'] = prod_json

        print("*****\n\n\n" , datas , "\n\n****\nn")
        return   JsonResponse(datas)
    
        
         







class about(views.View):
    def get(self , request):
        return render(request , 'selling/testimonial.html' )

    

    def post(self, request):
        pass




class contact(views.View):
    def get(self , request):
        datas = {}
        shop = models.shop.objects.all().first()
        datas['shop'] = shop
        mess_form = forms.message_in_contact()
        datas['message_form'] = mess_form





        return render(request , 'selling/contact.html'  , datas)

    

    def post(self, request):
        pass



class product_detail(views.View):
    def get(self , request):
        return render(request , 'selling/shop-detail.html' )

    

    

    def post(self, request):
        pass


class specific_product(views.View):
    

    def get(self , request , product_slug) : 
        datas = {}
        mess_form = forms.message_form()
        datas['message_form'] = mess_form 
        shop = models.shop.objects.all().first()
        datas['shop'] = shop

        prod = models.product.objects.filter(name = product_slug).first()
        datas['product'] = prod
        related_product = models.product.objects.all()[:7] 
        datas['relateds'] = related_product



        return render( request , 'selling/specific_product.html' , datas)




    def post(self , request , product_slug):
        pass