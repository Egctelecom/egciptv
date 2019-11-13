import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from crmadmin.forms import ManageServicesPriceForm, ManageServicesPriceCategoryForm
from crmadmin.models import ManageServicesPriceCategory, ManageServicePrice
from agentpanel.models import Agent

from django.contrib.auth.decorators import user_passes_test

def my_check(user):
    if Agent.objects.filter(user_id=user.id).exists():
        if user.is_superuser == False:
            data = True
            return data
#---------------------------------------------------------------------Servies Category Section----------------------------------------

#add

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def settings_manage_service_price_category_add(request):
    if request.method == 'GET':
        return render(request, 'agent/settings/manage_service_price/category/category_add.html')
    elif request.method == 'POST':
        form = ManageServicesPriceCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Service Category added successfully')
            return HttpResponseRedirect(reverse('agent_settings_manage_service_price_category_add'))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('agent_settings_manage_service_price_category_add'))

#edit

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def settings_manage_service_price_category_edit(request,pk):
    if request.method == 'GET':
        servies_category = ManageServicesPriceCategory.objects.values('id','service_category_name','status')
        return render(request, 'agent/settings/manage_service_price/category/category_edit.html',{'servies_category':servies_category})
    elif request.method == 'POST':
        form = ManageServicesPriceCategoryForm(request.POST)
        data = ManageServicesPriceCategory.objects.get(pk=pk)
        if form.is_valid():
            data.service_category_name = form['agent_service_category_name'].data
            data.status = form['status'].data
            data.save()
            messages.add_message(request, messages.SUCCESS, 'Service Category edited successfully')
            return HttpResponseRedirect(reverse('agent_settings_manage_service_price_category_edit',kwargs={'pk': pk}))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('agent_settings_manage_service_price_category_edit',kwargs={'pk': pk}))

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def settings_manage_service_price_category_delete(request,pk):
    if request.method == 'GET':
        if ManageServicesPriceCategory.objects.filter(pk=pk).exists():
            ManageServicesPriceCategory.objects.filter(pk=pk).delete()
            ManageServicesPriceCategory.objects.values('id','service_category_name','status')
            messages.add_message(request, messages.SUCCESS, 'Service Category edited successfully')
            return HttpResponseRedirect(reverse('settings'))
        else:
            messages.add_message(request, messages.ERROR,'Error Occure')
            return HttpResponseRedirect(reverse('agent_settings'))



#-------------------------------------------------------------------Servies Section------------------------------------------------

#add

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def settings_manage_service_price_add(request,category_id):
    if request.method == 'GET':
        servies_category = ManageServicesPriceCategory.objects.values('id', 'service_category_name', 'status').filter(pk=category_id)
        return render(request, 'agent/settings/manage_service_price/servies/services_add.html',{'servies_category':servies_category})
    elif request.method == 'POST':
        form = ManageServicesPriceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Service added successfully')
            return HttpResponseRedirect(reverse('agent_settings_manage_service_price_add',kwargs={'category_id':category_id}))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('agent_settings_manage_service_price_add',kwargs={'category_id':category_id}))

# edit

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def settings_manage_service_price_edit(request, pk,category_id):
       print(category_id)
       if request.method == 'GET':
            servies_category = ManageServicesPriceCategory.objects.values('id', 'service_category_name', 'status').filter(pk=category_id)
            servies = ManageServicePrice.objects.values('id', 'service_name','service_price','service_category_id','status').filter(pk=pk)
            return render(request, 'agent/settings/manage_service_price/servies/services_edit.html',
                          {'servies': servies,'servies_category':servies_category,'category_id':category_id})
       elif request.method == 'POST':
            form = ManageServicesPriceForm(request.POST)
            try:
                data = ManageServicePrice.objects.get(pk=pk)
                if form.is_valid():
                    data.service_category_id = form['service_category'].data
                    data.service_name = form['service_name'].data
                    data.service_price = form['service_price'].data
                    data.status = form['status'].data
                    data.save()
                    messages.add_message(request, messages.SUCCESS, 'Service Edited successfully')
                    return HttpResponseRedirect(reverse('agent_settings_manage_service_price_edit', kwargs={'pk':pk,'category_id':category_id}))
                else:
                    messages.add_message(request, messages.ERROR, form.errors)
                    return HttpResponseRedirect(reverse('agent_settings_manage_service_price_edit', kwargs={'pk': pk,'category_id':category_id}))

            except ManageServicePrice.DoesNotExist:
                data = None
                messages.add_message(request, messages.ERROR, 'Error')
                return HttpResponseRedirect(reverse('agent_settings_manage_service_price_edit', kwargs={'pk': pk,'category_id':category_id}))

#delete
@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def settings_manage_service_price_delete(request,pk):
    if request.method == 'GET':
        if ManageServicePrice.objects.filter(pk=pk).exists():
            ManageServicePrice.objects.filter(pk=pk).delete()
            messages.add_message(request, messages.SUCCESS, 'Service Deleted successfully')
            return HttpResponseRedirect(reverse('agent_settings'))
        else:
            messages.add_message(request, messages.ERROR, 'Error Occure')
            return HttpResponseRedirect(reverse('agent_settings'))

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def settings_manage_service_price_value_update(request):
    if request.is_ajax():
        price = request.POST['service_price']
        pk = request.POST['pk']
        if ManageServicePrice.objects.filter(pk=pk).exists():
            try :
                data = ManageServicePrice.objects.get(pk=pk)
                data.service_price = price
                data.save()
                msg = price
                return HttpResponse(json.dumps({"data": msg}), content_type="application/json")

            except ManageServicePrice.DoesNotExist:
                msg = 'Your Password Be changed'
                return HttpResponse(json.dumps({"data": msg}), content_type="application/json")

        else:
            msg = 'New password and confirm password should be matched'
            return HttpResponse(json.dumps({"data": msg}), content_type="application/json")

#--------------------------------------------------- Service TAB SET ---------------------------------------------------------

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def set_tab(request):
    if request.is_ajax():
        request.session['tabName'] = request.POST['tabName']
        return HttpResponse(request.session['tabName'])

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def set_tab_col(request):
    if request.is_ajax():
        request.session['tabNamecol'] = request.POST['tabName']
        return HttpResponse(request.session['tabNamecol'])
