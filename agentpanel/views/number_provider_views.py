import json
import http.client

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse
from agentpanel.models import Agent
from adminnumberprovider.models import NumberProvinceMap, NumberProvinceCustomerMap
from adminsidecustomer.models import Country, Province
from django.contrib.auth.decorators import user_passes_test

def my_check(user):
    if Agent.objects.filter(user_id=user.id).exists():
        if user.is_superuser == False:
            data = True
            return data

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def index(request):
 if request.method == 'GET':
     number = NumberProvinceMap.objects.values('province_id','country_id','did_id','npa','nxx','xxxx','tier','ratecenters','number','setup_rate','monthly_rate','per_minute_rate')
     return render(request, 'agent/number/index.html',{'number': number})

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def add(request):
    if request.method == 'GET':
        country_list = Country.objects.values('id', 'country_name')
        return render(request, 'agent/number/add.html',{'country_list':country_list})
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

#=================================================================== Get Ratecenters ======================================================#

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def get_province_via(request):
    if request.is_ajax():
         province = Province.objects.values('id', 'province_name').filter(country_id_id=request.POST['country'])
         data = render_to_string('agent/number/list.html',{'province': province})
         return HttpResponse(json.dumps({'data': data}), content_type="application/json")

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
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
        data = render_to_string('agent/number/ratearrlist.html', {'ratearr': ratearr})
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
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
        numberarr = []
        for rate in number['data']['dids']:
            numberarr.append(rate['number'])
            numberarr.append(rate['id'])

        datalist = []
        for rate in number['data']['dids']:
            datalist.append(rate)
        request.session['datalist']=datalist

        data = render_to_string('agent/number/numberarrlist.html', {'numberarr': numberarr})
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")


#================================================ MAP TO USER ===========================================================================


@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def map_number_to_user(request,id):
    if request.method == 'GET':
        number_data = NumberProvinceMap.objects.values('id','province_id','country_id','did_id','npa','nxx','xxxx','tier','ratecenters','number','setup_rate','monthly_rate','per_minute_rate')
        return render(request, 'agent/number/user/map_to_user.html',{'id':id,'number_data':number_data})
    elif request.method == 'POST':
        if  NumberProvinceCustomerMap.objects.filter(user_id=id,number_id=request.POST['number']).exists():

            messages.add_message(request, messages.SUCCESS, 'This Number already used')
            return HttpResponseRedirect(reverse('agent_map_number_to_user', kwargs={'id': id}))

        else:

            NumberProvinceCustomerMap.objects.create(user_id=id,number_id=request.POST['number'])
            messages.add_message(request, messages.SUCCESS, 'This Number added to user')
            return HttpResponseRedirect(reverse('agent_map_number_to_user',kwargs={'id':id}))

