import json
import http.client

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from adminnumberprovider.models import NumberProvinceMap, NumberProvinceCustomerMap
from adminsidecustomer.models import Country, Province,AccountAddressCustomer
from django.contrib.auth.decorators import user_passes_test

def my_check(user):
    return user.is_superuser == True


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def index(request):
 if request.method == 'GET':
     number = NumberProvinceMap.objects.values('province_id','country_id','did_id','npa','nxx','xxxx','tier','ratecenters','number','setup_rate','monthly_rate','per_minute_rate')
     return render(request, 'admin/number/index.html',{'number': number})

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def add(request):
    if request.method == 'GET':
        country_list = Country.objects.values('id', 'country_name')
        return render(request, 'admin/number/add.html',{'country_list':country_list})
    elif request.method == 'POST':
        if NumberProvinceMap.objects.filter(number=request.POST['number']).exists():
            messages.add_message(request, messages.SUCCESS, 'This Number already added')
            return HttpResponseRedirect(reverse('number_add'))
        else:
            data = request.session['datalist']
            arry = []
            for dt in data:
                if dt['number'] == request.POST['number']:
                    arry.append(dt)
            print(arry)
            for dr in arry:
                NumberProvinceMap.objects.create(province_id=request.POST['province'],
                                                 country_id=request.POST['country'],
                                                 did_id=dr['id'],
                                                 number=dr['number'],
                                                 npa=dr['npa'],
                                                 nxx=dr['nxx'],
                                                 xxxx=dr['xxxx'],
                                                 ratecenters=dr['ratecenter'],
                                                 tier=dr['tier'],
                                                 setup_rate=dr['setup_rate'],
                                                 monthly_rate=dr['monthly_rate'],
                                                 per_minute_rate=dr['per_minute_rate']
                                                 )
            messages.add_message(request, messages.SUCCESS, 'This Number added to provider')
            return HttpResponseRedirect(reverse('number_add'))

#===============================================================================  Get Ratecenters =====================================================================================================================#

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def get_province_via(request):
    if request.is_ajax():
         province = Province.objects.values('id', 'province_name').filter(country_id_id=request.POST['country'])
         data = render_to_string('admin/number/list.html',{'province': province})
         return HttpResponse(json.dumps({'data': data}), content_type="application/json")

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def get_ratecenters(request):
    if request.is_ajax():

        conn = http.client.HTTPSConnection("apiv1.teleapi.net")

        headers = {
            'cache-control': "no-cache",
            'postman-token': "135679ed-7c4a-eeea-737f-bd48de9223cc"
        }

        conn.request("POST", "/dids/states?token=73ad3b26-88a2-4f59-90ae-9be6a256782d", headers=headers)

        res = conn.getresponse()
        data = res.read()
        ft = json.loads(data.decode("utf-8"))
        datarate = ft['data']
        keys = []
        province = Province.objects.values('province_name').filter(id=request.POST['province'])
        for key, value in datarate.items():
            if province[0]['province_name'] == value:
                keys.append(key)
        conn2 = http.client.HTTPSConnection("apiv1.teleapi.net")

        headers2 = {
            'cache-control': "no-cache",
            'postman-token': "1f44f19e-dac4-458e-1111-9c581e3682d2"
        }

        conn2.request("POST", "/dids/ratecenters?token=73ad3b26-88a2-4f59-90ae-9be6a256782d&state="+keys[0], headers=headers2)

        res = conn2.getresponse()
        data = res.read()
        ratecenter = json.loads(data.decode("utf-8"))
        ratearr = []
        for rate in ratecenter['data']:
            ratearr.append(rate['ratecenter'])
        request.session['state']=keys[0]
        data = render_to_string('admin/number/ratearrlist.html', {'ratearr': ratearr})
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def get_number(request):
    if request.is_ajax():
        conn = http.client.HTTPSConnection("apiv1.teleapi.net")

        headers = {
            'cache-control': "no-cache",
            'postman-token': "8a74dbf9-a221-9250-c131-dc45cfb6823d"
        }

        conn.request("POST", "/dids/list?token=73ad3b26-88a2-4f59-90ae-9be6a256782d&state="+request.session['state']+"&ratecenter="+request.POST['ratecenter'],
                     headers=headers)

        res = conn.getresponse()
        data = res.read()
        number = json.loads(data.decode("utf-8"))
        print(number)
        numberarr = []
        for rate in number['data']['dids']:
            numberarr.append(rate['number'])
            numberarr.append(rate['id'])

        datalist = []
        for rate in number['data']['dids']:
            datalist.append(rate)
        request.session['datalist']=datalist

        data = render_to_string('admin/number/numberarrlist.html', {'numberarr': numberarr})
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")


#======================================================================================== MAP TO USER =====================================================================================================


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def map_number_to_user(request,id):
    if request.method == 'GET':
        user_address =  AccountAddressCustomer.objects.values('id', 'address_1', 'address_2', 'city_id__city_name','province_id','country_id',
                                              'province_id__province_name', 'country_id__country_name').filter(
            user_id=id)
        number_data = NumberProvinceMap.objects.values('id','province_id','country_id','did_id','npa','nxx',
                                                       'xxxx','tier','ratecenters','number','setup_rate','monthly_rate',
                                                       'per_minute_rate').filter(province_id=user_address[0]['province_id'],country_id=user_address[0]['country_id'])
        
        return render(request, 'admin/number/user/map_to_user.html',{'id':id,'number_data':number_data})
    elif request.method == 'POST':
        if  NumberProvinceCustomerMap.objects.filter(user_id=id,number_id=request.POST['number']).exists():

            messages.add_message(request, messages.SUCCESS, 'This Number already used')
            return HttpResponseRedirect(reverse('map_number_to_user', kwargs={'id': id}))

        else:
    
            numBER = NumberProvinceMap.objects.values('id', 'province_id', 'country_id', 'did_id', 'npa', 'nxx', 'xxxx', 'tier',
                                             'ratecenters', 'number', 'setup_rate', 'monthly_rate', 'per_minute_rate').filter(pk=request.POST['number'])



            conn = http.client.HTTPSConnection("apiv1.teleapi.net")

            headers = {
                'cache-control': "no-cache",
                'postman-token': "630db1d8-6928-cba2-5804-4cb90074787a"
            }

            conn.request("POST", "/dids/order?token=73ad3b26-88a2-4f59-90ae-9be6a256782d&number="+numBER[0]['number'],
                         headers=headers)

            res = conn.getresponse()
            data = res.read()
            ft = json.loads(data.decode("utf-8"))
            # ft = json.loads('{"code": 200,"status": "success","data": {"id": "15761561","user_id": "2159","call_flow_id": "3023","channel_group_id": null,"voicemail_inbox_id": null,
            # "number": "5876000948","country_code": "1","npa": "587","nxx": "600", "xxxx": "948","number_type": "local","state": "AB","ratecenter": "AIRDRIE","sms_enabled": "1","cnam": "disabled"}}')
            # datarate = ft['data']
            datastatus = ft['status']
            if datastatus == "success":
                NumberProvinceCustomerMap.objects.create(user_id=id,number_id=request.POST['number'])
                messages.add_message(request, messages.SUCCESS, 'This Number added to user')
                return HttpResponseRedirect(reverse('map_number_to_user',kwargs={'id':id}))
            else:
                messages.add_message(request, messages.SUCCESS, 'You can not map this number. It is unavailable.')
                return HttpResponseRedirect(reverse('map_number_to_user', kwargs={'id': id}))

