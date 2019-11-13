from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from adminsidecustomer.models import Country
from adminsidecustomer.models import Province
from adminsidecustomer.models import City
from django.template.loader import render_to_string
import json
from django.contrib.auth.decorators import user_passes_test

def my_check(user):
    return user.is_superuser == True
#================================== Optional ===================================================================#
@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def add(request):
 if request.method == 'GET':
    country = Country.objects.values('id','country_name')
    arr =['Saskatchewan','Yukon Territory']
    for arrlist in arr:
     data = Province.objects.create(country_id_id=country[0]['id'],province_name=arrlist)
    return HttpResponse(data)

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def city_add(request):
 if request.method == 'GET':
    id = 0
    province = Province.objects.values('id','province_name').filter(pk=id)
    data = City.objects.create(province_id_id=province[0]['id'],city_name='montreal')
    return HttpResponse(data)

#================================================================================================================#

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def get_province(request):
    if request.is_ajax():
         province = Province.objects.values('id','province_name').filter(country_id_id=request.POST['country'])
         data = render_to_string('admin/users/list.html',{'province': province})
         return HttpResponse(json.dumps({'data': data}), content_type="application/json")
    
def get_service_province(request):
    if request.is_ajax():
         province = Province.objects.values('id','province_name').filter(country_id_id=request.POST['country'])
         data = render_to_string('admin/users/list.html',{'province': province})
         return HttpResponse(json.dumps({'data': data}), content_type="application/json")



@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def get_city(request):
    if request.is_ajax():
         city = City.objects.values('id','city_name').filter(province_id_id=request.POST['province'])
         data = render_to_string('admin/users/citylist.html',{'city': city})
         return HttpResponse(json.dumps({'data': data}), content_type="application/json")



@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def get_billing_province(request):
    if request.is_ajax():
         province = Province.objects.values('id','province_name').filter(country_id_id=request.POST['country'])
         data = render_to_string('admin/users/probillist.html',{'province': province})
         return HttpResponse(json.dumps({'data': data}), content_type="application/json")


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def get_billing_city(request):
    if request.is_ajax():
         city = City.objects.values('id','city_name').filter(province_id_id=request.POST['province'])
         data = render_to_string('admin/users/citybilllist.html',{'city': city})
         return HttpResponse(json.dumps({'data': data}), content_type="application/json")