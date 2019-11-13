import json
from django.template.loader import render_to_string
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render
from django.urls import reverse

from crmadmin.forms import ManageServicesPriceForm, ManageServicesPriceCategoryForm,ManageServicePricedocForm
from crmadmin.models import ManageServicesPriceCategory, ManageServicePrice
from adminsideserviceprovider.models import ManageServicePricedoc
from django.utils.datastructures import MultiValueDictKeyError

#---------------------------------------------------------------------Servies Category Section----------------------------------------

#add

from django.contrib.auth.decorators import user_passes_test

def my_check(user):
    return user.is_superuser == True

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def settings_manage_service_price_category_add(request):
    if request.method == 'GET':
        return render(request, 'admin/settings/manage_service_price/category/category_add.html')
    elif request.method == 'POST':
        form = ManageServicesPriceCategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Service Category added successfully')
            return HttpResponseRedirect(reverse('settings_manage_service_price_category_add'))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('settings_manage_service_price_category_add'))

#edit

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def settings_manage_service_price_category_edit(request,pk):
    if request.method == 'GET':
        servies_category = ManageServicesPriceCategory.objects.values('id','service_category_name','status').filter(pk=pk)
        return render(request, 'admin/settings/manage_service_price/category/category_edit.html',{'servies_category':servies_category})
    elif request.method == 'POST':
        form = ManageServicesPriceCategoryForm(request.POST)
        data = ManageServicesPriceCategory.objects.get(pk=pk)
        if form.is_valid():
            data.service_category_name = form['service_category_name'].data
            data.status = form['status'].data
            data.save()
            messages.add_message(request, messages.SUCCESS, 'Service Category edited successfully')
            return HttpResponseRedirect(reverse('settings_manage_service_price_category_edit',kwargs={'pk': pk}))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('settings_manage_service_price_category_edit',kwargs={'pk': pk}))

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def settings_manage_service_price_category_delete(request,pk):
    if request.method == 'GET':
        if ManageServicesPriceCategory.objects.filter(pk=pk).exists():
            ManageServicesPriceCategory.objects.filter(pk=pk).delete()
            ManageServicesPriceCategory.objects.values('id','service_category_name','status')
            messages.add_message(request, messages.SUCCESS, 'Service Category edited successfully')
            return HttpResponseRedirect(reverse('settings'))
        else:
            messages.add_message(request, messages.ERROR,'Error Occure')
            return HttpResponseRedirect(reverse('settings'))



#-------------------------------------------------------------------Servies Section------------------------------------------------

#add

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def settings_manage_service_price_add(request,category_id):
    if request.method == 'GET':
        servies_category = ManageServicesPriceCategory.objects.values('id', 'service_category_name', 'status').filter(pk=category_id)
        return render(request, 'admin/settings/manage_service_price/servies/services_add.html',{'servies_category':servies_category})
    elif request.method == 'POST':
        form = ManageServicesPriceForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()

            messages.add_message(request, messages.SUCCESS, 'Service added successfully')
            return HttpResponseRedirect(reverse('settings_manage_service_price_add',kwargs={'category_id':category_id}))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('settings_manage_service_price_add',kwargs={'category_id':category_id}))

# edit

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def settings_manage_service_price_edit(request, pk,category_id):
       if request.method == 'GET':
            servies_category = ManageServicesPriceCategory.objects.values('id', 'service_category_name', 'status').filter(pk=category_id)
            servies = ManageServicePrice.objects.values('id', 'service_name','service_price','service_category_id','status','service_desc').filter(pk=pk)
            return render(request, 'admin/settings/manage_service_price/servies/services_edit.html',
                          {'servies': servies,'servies_category':servies_category,'category_id':category_id})
       elif request.method == 'POST':
            Ser = ManageServicePrice.objects.values('id', 'service_name','service_price','service_category_id','status','service_desc','service_logo').filter(pk=pk)

            form = ManageServicesPriceForm(request.POST,request.FILES)
            try:
                data = ManageServicePrice.objects.get(pk=pk)
                if form.is_valid():
                    if len(request.FILES) != 0:
                        data.service_category_id = form['service_category'].data
                        data.service_name = form['service_name'].data
                        data.service_price = form['service_price'].data
                        data.service_desc = form['service_desc'].data
                        data.service_logo = request.FILES['service_logo']
                        data.special_offer = form['special_offer'].data
                        data.status = form['status'].data
                        data.save()
                        messages.add_message(request, messages.SUCCESS, 'Service Edited successfully')
                        return HttpResponseRedirect(reverse('settings_manage_service_price_edit', kwargs={'pk':pk,'category_id':category_id}))
                    else:
                        data.service_category_id = form['service_category'].data
                        data.service_name = form['service_name'].data
                        data.service_price = form['service_price'].data
                        data.service_desc = form['service_desc'].data
                        data.service_logo = Ser[0]['service_logo']
                        data.special_offer = form['special_offer'].data
                        data.status = form['status'].data
                        data.save()
                        messages.add_message(request, messages.SUCCESS, 'Service Edited successfully')
                        return HttpResponseRedirect(reverse('settings_manage_service_price_edit',
                                                            kwargs={'pk': pk, 'category_id': category_id}))
                        
                else:
                    messages.add_message(request, messages.ERROR, form.errors)
                    return HttpResponseRedirect(reverse('settings_manage_service_price_edit', kwargs={'pk': pk,'category_id':category_id}))
                
            except ManageServicePrice.DoesNotExist:
                data = None
                messages.add_message(request, messages.ERROR, 'Error')
                return HttpResponseRedirect(reverse('settings_manage_service_price_edit', kwargs={'pk': pk,'category_id':category_id}))

#delete
@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def settings_manage_service_price_delete(request,pk):
    if request.method == 'GET':
        if ManageServicePrice.objects.filter(pk=pk).exists():
            ManageServicePrice.objects.filter(pk=pk).delete()
            messages.add_message(request, messages.SUCCESS, 'Service Deleted successfully')
            return HttpResponseRedirect(reverse('settings'))
        else:
            messages.add_message(request, messages.ERROR, 'Error Occure')
            return HttpResponseRedirect(reverse('settings'))

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
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

# =============================================== Service Provider Doc ================================================

# Doc Add

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def settings_manage_service_price_doc_add(request,id):
    if request.method == 'GET':
        return render(request, 'admin/settings/manage_service_price/servies/add_service_price_doc.html',{'id':id})
    elif request.method =='POST':
        forms = ManageServicePricedocForm(request.POST,request.FILES)
        if forms.is_valid():
            forms.save()
            messages.add_message(request, messages.SUCCESS, 'Document Uploaded successfully')
            return HttpResponseRedirect(reverse('settings_manage_service_price_doc_add',kwargs={'id':id}))
        else:
            messages.add_message(request, messages.ERROR, forms.errors)
            return HttpResponseRedirect(reverse('settings_manage_service_price_doc_add',kwargs={'id':id}))

# Doc view

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def settings_manage_service_price_doc_view(request, id):
    if request.method == 'GET':
        data = ManageServicePricedoc.objects.values('id','service_price_doc_name','service_price_doc','status','created_at','service_price_provider_id').filter(service_price_provider_id=id)
        return render(request, 'admin/settings/manage_service_price/servies/service_price_doc_view.html',
                      {'id': id,'data':data})
    

# Doc Delete

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def settings_manage_service_price_doc_delete(request,id,service_provider_id):
    if request.method == 'GET':
        if ManageServicePricedoc.objects.filter(pk=id).exists():
            ManageServicePricedoc.objects.filter(pk=id).delete()
            messages.add_message(request, messages.SUCCESS, 'Document deleted successfully')
            return HttpResponseRedirect(reverse('settings_manage_service_price_doc_view',kwargs={'id':service_provider_id}))
        else:
            # messages.add_message(request, messages.ERROR, forms.errors)
            return HttpResponseRedirect(reverse('settings_manage_service_price_doc_view',kwargs={'id':service_provider_id}))
    
# DOC status change

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def settings_manage_service_price_doc_status_change(request):
    if request.is_ajax:
            id = request.POST['id']
            if ManageServicePricedoc.objects.filter(pk=id).exists():
                msc = ManageServicePricedoc.objects.values('id','status').filter(pk=id)
                if msc[0]['status'] == 'active':
                    data = ManageServicePricedoc.objects.get(pk=id)
                    data.status='inactive'
                    data.save()
                    msg = 'Status Updated successfully as '+ ' '+data.status+'. Now you can not show download button in front end section.'
                    msc = ManageServicePricedoc.objects.values('id', 'status').filter(pk=id)
                    data = render_to_string('admin/settings/manage_service_price/servies/list.html', {'msc': msc})
                    return HttpResponse(json.dumps({"data": data,"msg":msg}), content_type="application/json")
                else:
                    data = ManageServicePricedoc.objects.get(pk=id)
                    data.status = 'active'
                    data.save()
                    msg = 'Status Updated successfully as '+ ' '+data.status+'. Now you can show download button in front end section.'
                    msc = ManageServicePricedoc.objects.values('id', 'status').filter(pk=id)
                    data = render_to_string('admin/settings/manage_service_price/servies/list.html', {'msc': msc})
                    return HttpResponse(json.dumps({"data": data,"msg":msg}), content_type="application/json")
                    
            else:
                msg = 'Warning ! Your documents does not exists.'
                return HttpResponse(json.dumps({"data": msg}), content_type="application/json")
    
#--------------------------------------------------- Service TAB SET ---------------------------------------------------------

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def set_tab(request):
    if request.is_ajax():
        del request.session['tabName']
        if request.POST['tabName'] == 'manage_service_prices':
            request.session['tabName'] = 'manage_service_prices'
        else:
            request.session['tabName'] = 'logins'
        # request.session['tabName'] = request.POST['tabName']
        return HttpResponse(request.session['tabName'])

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def set_tab_col(request):
    if request.is_ajax():
        request.session['tabNamecol'] = request.POST['tabName']
        return HttpResponse(request.session['tabNamecol'])
