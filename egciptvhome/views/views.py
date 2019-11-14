from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import *
from django.http import JsonResponse
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from adminsidecustomer.models import Customer, AccountAddressCustomer, BillingAddressCustomer, BillingDetailsCustomer, \
    CutomerAttachmentMap, CustomerUserMap,Country,Province,City
from adminsideserviceprovider.models import CustomerTicketsCategoriesMap,ServiceProviderCityMap
from adminsideserviceprovider.models import ServiceProvider, ServiceProviderPlan, CustomerWithService,CustomerServiceContract
from sitefrontendbyadmin.models import MenuParentCategory, serviceandfeature, Slider, Network_status, FAQ, Followus, \
    SpecialoffersUnderCategory
from crmadmin.models import ManageServicesPriceCategory, ManageServicePrice
import requests
import json
from egciptvhome.models import Otherdetails
from django.core.mail import send_mail, EmailMessage
from ratecustomerbillingwithcdr.models import VoipLongDistanceRate
import re


def index(request):
    servies_category = ManageServicesPriceCategory.objects.values('id', 'service_category_name', 'status').filter(status='active')
    service_feature = serviceandfeature.objects.values('id',
                                                       'service_parent_category_id',
                                                       'service_category_id__service_category_name',
                                                       'service_parent_category_id__service_parent_category_name',
                                                       'service_sub_parent_category_name_id',
                                                       'details',
                                                       'service_feature_logo',
                                                       'service_sub_parent_category_name_id__service_sub_parent_category_name').filter(status='active')
    
    
    follow_us = Followus.objects.values('id', 'url', 'fa_fa_icon', 'status').filter(status='active')
    slider = Slider.objects.values('id', 'slider_name', 'details', 'image', 'url', 'status').filter(status='active')
    special_offers = SpecialoffersUnderCategory.objects.filter(status='active')
    distinct_special_offers = SpecialoffersUnderCategory.objects.distinct('special_offers_type_name').values('special_offers_type_name')
    print(distinct_special_offers)
    
    return render(request, 'egciptv/index.html', {'servies_category': servies_category,
                                                  'service_feature': service_feature,
                                                  'slider': slider,
                                                  'follow_us': follow_us,
                                                  'special_offers': special_offers,
                                                  'distinct_special_offers': distinct_special_offers
                                                  })


def customer_login(request):
    if request.method == "GET":
        return render(request, 'egciptv/login.html')
    elif request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username= username, password= password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse(my_account,kwargs={'pk':user.id}))
        else:
            pass
        return HttpResponseRedirect(reverse(index))


@login_required(login_url=customer_login)
def my_account(request,pk):
    if request.method == "GET":
        customer = CustomerUserMap.objects.values('user_id',
                                                  'customer_id',
                                                  'customer_id__id',
                                                  'customer_id__account_id',
                                                  'customer_id__status',
                                                  'customer_id__first_name',
                                                  'customer_id__first_name_gsr',
                                                  'customer_id__last_name',
                                                  'customer_id__last_name_gsr',
                                                  'customer_id__company_name',
                                                  'customer_id__company_name_gsr',
                                                  'customer_id__portal_password',
                                                  'customer_id__email_address',
                                                  'customer_id__phone',
                                                  'customer_id__other_phone',
                                                  'customer_id__dob',
                                                  'customer_id__display_name',
                                                  'customer_id__prefferd_language',
                                                  'customer_id__zone',
                                                  'customer_id__created_at'
                                                  ).filter(user_id=pk)
        
        
        
        return render(request, 'egciptv/profile.html',{'customer':customer})


@login_required(login_url=customer_login)
def user_logout(request):
    if request.method == "GET":
        logout(request)
        return HttpResponseRedirect(reverse(index))


#====================================================================================== Other Pages =============================================================================================#


def other_services(request):
    if request.method == "GET":
        id = request.user
        array_of_id = []
        
        customer = CustomerUserMap.objects.values('user_id',
                                                  'customer_id').filter(user_id=id)
        
        city = AccountAddressCustomer.objects.values('city_id').filter(user_id=customer[0]['customer_id'])
        
        city_service = ServiceProviderCityMap.objects.values('service_provider_id').filter(city_id=city[0]['city_id'])
        
        for city_services in city_service:
            array_of_id.append(city_services['service_provider_id'])
        
        services = ServiceProvider.objects.values('id', 'service_provider_name').filter(id__in=array_of_id)
        services_provider_with_plan = ServiceProviderPlan.objects.values(
            'id',
            'service_provider_id__service_provider_name',
            'service_provider_id',
            'title',
            'retail',
            'actual',
            'qty'
        ).filter(service_provider_id__in=array_of_id)
        
        
        return render(request, 'egciptv/other-service.html',{'services':services,'services_provider_with_plan':services_provider_with_plan})

def contact_us(request):
    if request.method == "GET":
        other_details = Otherdetails.objects.values('id', 'key', 'value','address','country', 'city', 'province', 'zip', 'fax',
                                                    'phone', 'email').filter(key='Contact')
        return render(request, 'egciptv/contact_us.html',{'other_details':other_details})

def get_city_of_region(request):
    if request.is_ajax():
        
        province =  request.POST['province']
        city =  request.POST['city']
        country='Canada'
        
        
        request.session['country'] = country
        request.session['province'] = province
        request.session['city'] = city
        
        try:
            
            province_data = Province.objects.values('id','country_id','province_name').filter(pk=province,country_id__country_name=country)
            citylits = City.objects.values('id','city_name').filter(pk=city,province_id=province)
            
            request.session['city_id'] = city
            request.session['province_id'] = province
            request.session['country_id'] = province_data[0]['country_id']
            
            request.session['province_name'] = province_data[0]['province_name']
            request.session['city_name']= citylits[0]['city_name']
            #
            
            data = {
                "results": {
                    "status": 'Success'
                }}
            return JsonResponse(data, safe=False)
        
        except Exception in e :
            
            data = {
                "results": {
                    "status": 'Error',
                    "data":e
                }}
            
            return JsonResponse(data,safe=False)


def get_city_according_region(request):
    if request.is_ajax():
        
        province =  request.POST['province']
        city_data = City.objects.values('id','city_name').filter(province_id=province)
        
        data = render_to_string('egciptv/data/city_list.html',{'city_data': city_data})
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")


def reg_get_city_according_region(request):
    if request.is_ajax():
        province = request.POST['province']
        city_data = City.objects.values('id', 'city_name').filter(province_id=province)
        data = render_to_string('egciptv/data/reg/city_list.html', {'city_data': city_data})
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")

def reg_billing_get_city_according_region(request):
    if request.is_ajax():
        province = request.POST['province']
        city_data = City.objects.values('id', 'city_name').filter(province_id=province)
        data = render_to_string('egciptv/data/reg/billing/city_list.html', {'city_data': city_data})
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")


def special_offers_get_city_according_region(request):
    if request.is_ajax():
        province = request.POST['province']
        city_data = City.objects.values('id', 'city_name').filter(province_id=province)
        data = render_to_string('egciptv/data/special_offers/city_list.html', {'city_data': city_data})
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")


def special_offers_billing_get_city_according_region(request):
    if request.is_ajax():
        province = request.POST['province']
        city_data = City.objects.values('id', 'city_name').filter(province_id=province)
        data = render_to_string('egciptv/data/special_offers/billing/city_list.html', {'city_data': city_data})
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")



def check_session(request):
    if request.is_ajax():
        if 'city_id' not in request.session:
            data = {
                "results": {
                    "status": 'Success',
                }}
            
            return JsonResponse(data, safe=False)
        else:
            data = {
                "results": {
                    "status": 'Error',
                }}
            
            return JsonResponse(data, safe=False)

def set_lang_session(request):
    if request.is_ajax():
        try:
            request.session['lang'] = request.POST['language']
            if 'lang' not in request.session:
                data = {
                    "results": {
                        "status": 'Error',
                    }}
                
                return JsonResponse(data, safe=False)
            else:
                data = {
                    "results": {
                        "status": 'Success',
                    }}
                
                return JsonResponse(data, safe=False)
        
        except Exception in e:
            
            data = {
                "results": {
                    "status": 'Error',
                }}
            
            return JsonResponse(data, safe=False)



def send_contact_to_admin(request):
    if request.method == "POST":
        name=request.POST['name']
        email=request.POST['email']
        phone=request.POST['phone']
        content=request.POST['content']
        subject2 = 'A User send for contact purpose'
        to_email2 = User.objects.values('email', 'username').filter(is_superuser='True')
        
        massege = render_to_string('egciptv/mail/contactmail.html',
                                   {'name': name, 'email': email,'phone':phone,'msg':content})
        
        html_msg = render_to_string('egciptv/mail/contactmail.html',
                                    {'name': name, 'email': email, 'phone': phone, 'msg': content})
        
        send_mail(subject2, massege, 'support@25airport.com', [to_email2[0]['email']], fail_silently=False,
                  html_message=html_msg)
        
        messages.add_message(request, messages.SUCCESS,
                             'Your contact details send to egciptv.We get back to you as soon as possible.')
        return HttpResponseRedirect(reverse('contact_us'))


def details(request,pk):
    if request.method == "GET":
        service_feature = serviceandfeature.objects.values('id',
                                                           'service_parent_category_id',
                                                           'service_category_id__service_category_name',
                                                           'service_parent_category_id__service_parent_category_name',
                                                           'service_sub_parent_category_name_id',
                                                           'details',
                                                           'service_sub_parent_category_name_id__service_sub_parent_category_name').filter(pk=pk)
        return render(request, 'egciptv/service_features_deatils.html',
                      {'service_feature': service_feature})

# ====================================================================================== Network Status =============================================================================================#

def network_status(request):
    if request.method == "GET":
        network_status = Network_status.objects.values('id', 'questions', 'answers', 'docs', 'link')
        return render(request, 'egciptv/network_status.html',
                      {'network_status': network_status})




#====================================================================================== Faq =============================================================================================#

def faq(request):
    if request.method == "GET":
        faq = FAQ.objects.values('id', 'questions', 'answers', 'docs', 'link')
        return render(request, 'egciptv/faq.html',
                      {'faq': faq})

#====================================================================================== About Us =============================================================================================#

def about_us(request):
    if request.method == "GET":
        about_us = Otherdetails.objects.values('id', 'key', 'value').filter(key='About')
        return render(request, 'egciptv/about_us.html',{'about_us': about_us})

# ====================================================================================== Terms & Conditions =============================================================================================#

def termsandconditions(request):
    if request.method == "GET":
        t_c = Otherdetails.objects.values('id', 'key', 'value').filter(key='Terms&Conditions')
        return render(request, 'egciptv/terms&conditions.html', {'t_c': t_c})


def privacyandpolicy(request):
    if request.method == "GET":
        t_c = Otherdetails.objects.values('id', 'key', 'value').filter(key='PrivacyPolicy')
        return render(request, 'egciptv/privacyandpolicy.html', {'t_c': t_c})


def voip_rate(request):
    if request.method == "GET":
        text = "A"
        text = re.escape(text)  # make sure there are not regex specials
        data = VoipLongDistanceRate.objects.values('id', 'country', 'prefix', 'rate').filter(country__iregex=r"(^|\s)%s" % text)
        ar = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
        return render(request, 'egciptv/voip_rate/index.html',{'data':data,'arr':ar})
