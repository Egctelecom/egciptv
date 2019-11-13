import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.loader import render_to_string

from adminsidecustomer.models import City, Province, Country
from adminsideserviceprovider.forms import ServiceProviderform, ServiceProviderPlanform, ServicePlanWithHardwareform, \
    Hardwareform
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from adminsideserviceprovider.models import ServiceProvider, ServiceProviderCityMap, ServiceProviderPlan, \
    ServicePlanWithHardware, Hardware
from agentpanel.models import Agent
from crmadmin.models import ManageServicePrice, ManageServicesPriceCategory
from django.contrib.auth.decorators import user_passes_test
#================================================== Service Provider ====================================================

def my_check(user):
    if Agent.objects.filter(user_id=user.id).exists():
        if user.is_superuser == False:
            data = True
            return data

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def service_provider_index(request):
 if request.method == 'GET':
    service_provider = ServiceProvider.objects.values('id','service_provider_name')
    return render(request, 'agent/service_provider/index.html',{'service_provider':service_provider})

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def service_provider_add(request):
 if  request.method == 'GET':
     service_provider = ServiceProvider.objects.values('service_provider_name')
     return render(request, 'agent/service_provider/add.html',{'service_provider':service_provider})
 elif request.method == 'POST':
    form = ServiceProviderform(request.POST)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.SUCCESS, 'Service Provider Added successfully')
        return HttpResponseRedirect(reverse('service_provider_add'))
    else:
        messages.add_message(request, messages.ERROR, form.errors)
        return HttpResponseRedirect(reverse('service_provider_add'))

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def service_provider_edit(request,id):
 if  request.method == 'GET':
     service_provider = ServiceProvider.objects.values('id','service_provider_name')
     return render(request, 'agent/service_provider/edit.html',{'service_provider':service_provider})
 elif request.method == 'POST':
        data = ServiceProvider.objects.get(pk=id)
        form = ServiceProviderform(request.POST)
        if form.is_valid():
            data.service_provider_name = form['service_provider_name'].data
            data.save()
            messages.add_message(request, messages.SUCCESS, 'Service Provider Update successfully')
            return HttpResponseRedirect(reverse('service_provider_edit', kwargs={'id': id}))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('service_provider_edit', kwargs={'id': id}))



# Add plan for service provider

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def plan_add_to_service_provider(request,id):
    if request.method == 'GET':
     manage_category =  ManageServicesPriceCategory.objects.values('id','service_category_name','status')
     return render(request, 'agent/service_provider/plan/add.html',{'id':id,'manage_category':manage_category})
    elif request.method == 'POST':
     form = ServiceProviderPlanform(request.POST)
     if form.is_valid():
         form.save()
         messages.add_message(request, messages.SUCCESS, 'Service Provider Plan Added successfully')
         return HttpResponseRedirect(reverse('plan_add_to_service_provider',kwargs={'id':id}))
     else:
         messages.add_message(request, messages.ERROR, form.errors)
         return HttpResponseRedirect(reverse('plan_add_to_service_provider', kwargs={'id': id}))

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def view_plan_of_service_provider(request,id):
    data = ServiceProviderPlan.objects.values('id','service_provider_id','title','retail','actual','qty').filter(service_provider_id=id)
    return render(request, 'agent/service_provider/plan/view.html',
                  {'data': data})

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def plan_edit(request,id):
    if request.method == 'GET':
         data = ServiceProviderPlan.objects.values('id', 'service_provider_id', 'title', 'retail', 'actual',
                                                      'qty').filter(pk=id)
         manage_category = ManageServicesPriceCategory.objects.values('id', 'service_category_name', 'status')
         return render(request, 'agent/service_provider/plan/edit.html',{'id':id,'data':data,'manage_category':manage_category})
    elif request.method == 'POST':
     data = ServiceProviderPlan.objects.get(pk=id)
     form = ServiceProviderPlanform(request.POST)
     if form.is_valid():
         data.title = form['title'].data
         data.retail = form['retail'].data
         data.actual = form['actual'].data
         data.qty = form['qty'].data
         data.save()
         messages.add_message(request, messages.SUCCESS, 'Service Provider Plan Edit successfully')
         return HttpResponseRedirect(reverse('plan_edit',kwargs={'id':id}))
     else:
         messages.add_message(request, messages.ERROR, form.errors)
         return HttpResponseRedirect(reverse('plan_edit', kwargs={'id': id}))



@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def get_service_via_category(request):
    if request.is_ajax():
        response_data = {}
        data = request.POST['category']
        if ManageServicePrice.objects.filter(service_category_id=data).exists():
            manage_service_price = ManageServicePrice.objects.values('id', 'service_category_id', 'service_name',
                                                                     'service_price', 'status').filter(service_category_id=data)

            data = render_to_string('agent/service_provider/plan/list.html', {'manage_service_price': manage_service_price})
            return HttpResponse(json.dumps({'data': data}), content_type="application/json")


@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def get_service_name(request):
    if request.is_ajax():
        data = request.POST['service_id']
        manage_service_price = ManageServicePrice.objects.values('id', 'service_category_id', 'service_name',
                                                                 'service_price', 'status').filter(pk=data)
        response_data = {}
        response_data['result'] = manage_service_price[0]['service_name']
        return JsonResponse(response_data, safe=False)

#================================================== Service Provider With City Map ====================================================


@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def service_provider_with_city_index(request):
    if request.method == 'GET':
        province_list = Province.objects.values('id', 'province_name')
        return render(request, 'agent/service_provider/service_provider_city_map/index.html', {'province_list': province_list})


#Set city service provider

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def province_with_city(request,id):
    if request.method == 'GET':
        city_list = City.objects.values('id', 'city_name').filter(province_id=id)
        return render(request, 'agent/service_provider/service_provider_city_map/cityindex.html', {'city_list': city_list})




@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def set_service_provider(request,id):
    if request.method == 'GET':
        service_provider =  ServiceProvider.objects.values('id','service_provider_name')
        plist = City.objects.values('id', 'province_id__province_name','province_id','province_id__country_id').filter(pk=id)
        return render(request, 'agent/service_provider/service_provider_city_map/set_service.html', {'service_provider': service_provider,'id':id,'plist':plist})


@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def save_service_provider_to_city(request):
    if request.is_ajax():
        response_data = {}
        data = request.POST['arrt']
        data = json.loads(data)
        if Province.objects.filter(pk=request.POST['province']).exists():
             if Country.objects.filter(pk=request.POST['country']).exists():
                 for arrlist in data:
                     if ServiceProviderCityMap.objects.filter(
                             service_provider_id=arrlist,
                             city_id=request.POST['city'],
                             province_id=request.POST['province'],
                             country_id=request.POST['country']
                         ).exists():
                         response_data['result'] = 'error'

                     else:
                        ServiceProviderCityMap.objects.create(
                            city_id=request.POST['city'],
                            service_provider_id=arrlist,

                            province_id=request.POST['province'],
                            country_id=request.POST['country']
                        )

                        response_data['result'] = 'success'

                 return JsonResponse(response_data, safe=False)


#================================================== Add Hardware According to data plan ================================================
@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def view_hw_in_service_provider(request,id):
        if request.method == 'GET':
            request.session['plan_id'] = id
            data = ServicePlanWithHardware.objects.values('id','hw_id','hw_qty','hw_status','hw_id__hw_title').filter(service_plan_id=id)
            return render(request, 'agent/service_provider/hardware/index.html', {'id': id,'data':data})

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def add_hw_in_service_provider(request,id):
        if request.method == 'GET':
            hw = Hardware.objects.values('id','hw_title')
            return render(request, 'agent/service_provider/hardware/add.html', {'id': id,'hw':hw})
        elif request.method == 'POST':
            form = ServicePlanWithHardwareform(request.POST)
            if form.is_valid():
                form.save()
                messages.add_message(request, messages.SUCCESS, 'Hardware added according to Service Provider Plan  successfully')
                return HttpResponseRedirect(reverse('add_hw_in_service_provider', kwargs={'id': id}))
            else:
                messages.add_message(request, messages.ERROR, form.errors)
                return HttpResponseRedirect(reverse('add_hw_in_service_provider', kwargs={'id': id}))


@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def edit_hw_in_service_provider(request, id):
    if request.method == 'GET':
        plan_id = request.session['plan_id']
        data = ServicePlanWithHardware.objects.values('id','hw_title','hw_retail','hw_actual','hw_qty').filter(pk=id)
        return render(request, 'agent/service_provider/hardware/edit.html', {'id': id, 'plan_id':plan_id,'data': data})
    elif request.method == 'POST':
        data = ServicePlanWithHardware.objects.get(pk=id)
        form = ServicePlanWithHardwareform(request.POST)
        if form.is_valid():
            data.hw_title = form['hw_title'].data
            data.hw_retail = form['hw_retail'].data
            data.hw_actual = form['hw_actual'].data
            data.hw_qty = form['hw_qty'].data
            data.save()
            messages.add_message(request, messages.SUCCESS, 'Hardware updated according to Service Provider Plan  successfully')
            return HttpResponseRedirect(reverse('agent_edit_hw_in_service_provider', kwargs={'id': id}))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('agent_edit_hw_in_service_provider', kwargs={'id': id}))


@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def delete_hw_in_service_provider(request, id):
    if request.method == 'GET':
     if ServicePlanWithHardware.objects.filter(pk=id).exists():
         ServicePlanWithHardware.objects.filter(pk=id).delete()
         messages.add_message(request, messages.SUCCESS, 'Hardware updated according to Service Provider deleted  successfully')
         plan_id = request.session['plan_id']
         return HttpResponseRedirect(reverse('agent_view_hw_in_service_provider', kwargs={'id': plan_id}))
     else:
         plan_id = request.session['plan_id']
         messages.add_message(request, messages.ERROR, 'Not Exites')
         return HttpResponseRedirect(reverse('agent_view_hw_in_service_provider', kwargs={'id': plan_id}))


#================================================== Add Hardware List ================================================
@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def view_hw_list(request):
    if request.method == 'GET':
        hw = Hardware.objects.values('id','hw_title')
        print(hw)
        return render(request, 'agent/service_provider/hardware/list/index.html',{'hw':hw})

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def add_hw_list(request):
    if request.method == 'GET':
        return render(request, 'agent/service_provider/hardware/list/add.html')
    elif request.method == 'POST':
        form = Hardwareform(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Hardware added ')
            return HttpResponseRedirect(reverse('agent_add_hw_list'))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('agent_add_hw_list'))

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def edit_hw_list(request,id):
    if request.method == 'GET':
        hw = Hardware.objects.values('id', 'hw_title','type','model','mac','sn','ver','usrn','passu','adusr','adpass','dslusr',
                                     'dslpass','date_start','date_end', 'still_in_service','device_buy','device_rental',
                                     'montly_rent').filter(pk=id)
        return render(request, 'agent/service_provider/hardware/list/edit.html',{'hw':hw})
    elif request.method == 'POST':
        form = Hardwareform(request.POST)
        data = Hardware.objects.get(pk=id)
        if form.is_valid():
            data.hw_title=form['hw_title'].data
            data.type=form['type'].data
            data.model=form['model'].data
            data.mac=form['mac'].data
            data.sn=form['sn'].data
            data.ver=form['ver'].data
            data.usrn=form['usrn'].data
            data.passu=form['passu'].data
            data.adusr=form['adusr'].data
            data.adpass=form['adpass'].data
            data.dslusr=form['dslusr'].data
            data.dslpass=form['dslpass'].data
            data.hw_title=form['hw_title'].data
            data.date_start=form['date_start'].data
            data.date_end=form['date_end'].data
            data.still_in_service=form['still_in_service'].data
            data.device_buy=form['device_buy'].data
            data.device_rental=form['device_rental'].data
            data.montly_rent=form['montly_rent'].data
            data.save()
            messages.add_message(request, messages.SUCCESS, 'Hardware edited ')
            return HttpResponseRedirect(reverse('agent_edit_hw_list',kwargs={'id':id}))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('agent_edit_hw_list',kwargs={'id':id}))