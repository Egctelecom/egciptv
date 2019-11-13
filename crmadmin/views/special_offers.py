from django.shortcuts import render
from adminsideserviceprovider.models import ServiceProvider, ServiceProviderPlan, CustomerWithService,CustomerServiceContract,ServicePlanWithHardware
from django.contrib.auth.decorators import user_passes_test
from crmadmin.models import ManageServicesPriceCategory, ManageServicePrice
from crmadmin.forms import ManageServicesPriceForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from sitefrontendbyadmin.models import MenuParentCategory,MenuCategory,MenuSubParentCategory,SpecialOffers,SpecialOffersPlans,SpecialOffersPlanswithHardwareRates,Specialoffersdoc
from sitefrontendbyadmin.forms import SpecialOffersDocForm
from adminsideserviceprovider.models import Hardware
from crmadmin.forms import SpecialOffersform
from django.urls import reverse
from django.template.loader import render_to_string
import json

def my_check(user):
    return user.is_superuser == True


     
    
@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def index(request):
     if request.method == 'GET':
      special_offers = SpecialOffers.objects.values('id',
                                                    'details',
                                                    'features',
                                                    'actual_price',
                                                    'offers_price',
                                                    )
      return render(request, 'admin/frontend/special_offers/index.html',{'special_offers':special_offers})
      
     

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def special_offers_services_plan_add(request):
    if request.method == 'GET':
        manage_service_price = ManageServicePrice.objects.values('id', 'service_name','service_price','service_category_id','status','service_desc')
        return render(request, 'admin/frontend/special_offers/servies/special_offers_services_plan_add.html',{'manage_service_price':manage_service_price})
    elif request.method == 'POST':
            form = SpecialOffersform(request.POST)
            if form.is_valid():
                special = form.save()
                service_plan_list = request.POST['service_plan']
                service_plan_list = json.loads(service_plan_list)
                for serviceElement in service_plan_list:
                    SpecialOffersPlans.objects.create(special_offers_id=special.id, service_price_id=serviceElement)
                messages.add_message(request, messages.SUCCESS, 'Special Offers combo pack added successfully')
                return HttpResponseRedirect(reverse('special_offers_services_plan_add'))
            else:
                messages.add_message(request, messages.ERROR, form.errors)
                return HttpResponseRedirect(reverse('special_offers_services_plan_add'))
        
        
@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def special_offers_services_plan_edit(request,pk):
    if request.method == 'GET':
        sp = SpecialOffers.objects.values('id','details','features','actual_price','offers_price').filter(pk=pk)
        spPlans = SpecialOffersPlans.objects.values('id','service_price_id').filter(special_offers_id=pk)
        specialOffers=[]
        for s in spPlans:
            specialOffers.append(s['service_price_id'])
            
        manage_service_price = ManageServicePrice.objects.values('id', 'service_name', 'service_price',
                                                                 'service_category_id', 'status', 'service_desc')
        m=[]
        for mpS in manage_service_price:
            m.append(mpS['id'])
            
        return render(request, 'admin/frontend/special_offers/servies/special_offers_services_plan_edit.html',{'sp':sp,'m':m,'manage_service_price':manage_service_price,'specialOffers':specialOffers})
    elif request.method == 'POST':
            data = SpecialOffers.objects.get(pk=pk)
            form = SpecialOffersform(request.POST)
            if form.is_valid():
                data.details = form['details'].data
                data.features = form['features'].data
                data.actual_price = form['actual_price'].data
                data.offers_price = form['offers_price'].data
                data.save()
                service_plan_list = request.POST['service_plan']
                service_plan_list = json.loads(service_plan_list)
                ari=[]
                SpecialOffersPlans.objects.filter(special_offers_id=pk).delete()


                for serviceElement in service_plan_list:
                    SpecialOffersPlans.objects.create(special_offers_id=pk, service_price_id=serviceElement)

                messages.add_message(request, messages.SUCCESS, 'Special Offers combo pack updated successfully')
                return HttpResponseRedirect(reverse('special_offers_services_plan_edit',kwargs={'pk':pk}))
            else:
                messages.add_message(request, messages.ERROR, form.errors)
                return HttpResponseRedirect(reverse('special_offers_services_plan_edit',kwargs={'pk':pk}))
        
#Get all service plans according to special offers

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def special_offers_services_plan(request,pk):
    if request.method == 'GET':
       servies_offers = SpecialOffersPlans.objects.values('id', 'service_price_id__service_name','service_price_id').filter(special_offers_id=pk)
       return render(request, 'admin/frontend/special_offers/servies/special_offers_service_plan.html', {'servies_offers': servies_offers,'special_offers_id':pk})


#Get all service plans hardware list according to special offers

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def special_offers_services_plan_hardware(request,pk,special_offers_id):
    if request.method == 'GET':
         services_provider_plan_dt = ServiceProviderPlan.objects.values('id','manage_service_id').filter(manage_service_id=pk)
         servies_offers = ServicePlanWithHardware.objects.values('id','hw_id','hw_id__hw_title','hw_id__device_buy','hw_id__device_rental','hw_id__montly_rent').filter(service_plan_id=services_provider_plan_dt[0]['id'])
         return render(request, 'admin/frontend/special_offers/servies/special_offers_service_plan_hardware.html',{'servies_offers': servies_offers,
                                                                                                                   'special_offers_id':special_offers_id,
                                                                                                                   'service_plan_id':services_provider_plan_dt[0]['id'],
                                                                                                                   'service_price_id':pk
                                                                                                                   })
         
        
        


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def special_offers_services_plan_hardware_offer_price_add(request,pk,special_offers_id,service_plan_id,service_price_id):
    if request.method == 'GET':
        hw = Hardware.objects.values('id','hw_title','device_buy','device_rental','montly_rent').filter(pk=pk)
        return render(request, 'admin/frontend/special_offers/servies/add_hardware_price.html',
                      {'hw': hw,
                       'hw_id':pk,
                       'special_offers_id':special_offers_id,
                       'service_plan_id':service_plan_id,
                       'service_price_id':service_price_id
                       })
    elif request.method == 'POST':
        try:
            if SpecialOffersPlanswithHardwareRates.objects.filter(special_offers_id=special_offers_id,
                                                                   service_price_id=service_price_id,
                                                                   service_plan_id=service_plan_id,
                                                                   hw_id=pk).exists():
    
                messages.add_message(request, messages.SUCCESS,
                                     'Offer price already added for this perticular Hardware. You Can only edit')
                return HttpResponseRedirect(reverse('special_offers_services_plan_hardware_offer_price',
                                                    kwargs={'pk': pk, 'special_offers_id': special_offers_id,
                                                            'service_plan_id': service_plan_id,
                                                            'service_price_id': service_price_id}))
            else:
                SpecialOffersPlanswithHardwareRates.objects.create(special_offers_id=special_offers_id,
                                                                   service_price_id=service_price_id,
                                                                   service_plan_id=service_plan_id,
                                                                   hw_id=pk,
                                                                   device_buy=request.POST['device_buy'],
                                                                   device_rental=request.POST['device_rental'],
                                                                   montly_rent=request.POST['montly_rent'],
                                                                   hw_qty=request.POST['hw_qty'],
                                                                   offer_price=request.POST['offer_price']
                                                                   )
                messages.add_message(request, messages.SUCCESS,
                                     'Special Offers Hardware according to service plan added successfully')
                return HttpResponseRedirect(reverse('special_offers_services_plan_hardware_offer_price',
                                                    kwargs={'pk': pk, 'special_offers_id': special_offers_id,
                                                            'service_plan_id': service_plan_id,
                                                            'service_price_id': service_price_id}))
               
        except Exception as e:
            messages.add_message(request, messages.ERROR, e)
            return HttpResponseRedirect(reverse('special_offers_services_plan_hardware_offer_price',kwargs={'pk':pk,'special_offers_id':special_offers_id,'service_plan_id':service_plan_id,'service_price_id':service_price_id}))
   
   
   
@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def special_offers_services_plan_hardware_offer_price_editorview(request,pk,special_offers_id,service_plan_id,service_price_id):
    if request.method == 'GET':
        hw = Hardware.objects.values('id','hw_title','device_buy','device_rental','montly_rent').filter(pk=pk)
        spOffershw = SpecialOffersPlanswithHardwareRates.objects.values('special_offers_id','service_price_id','service_plan_id','hw_id','device_buy','device_rental','montly_rent','hw_qty','offer_price').filter(special_offers_id=special_offers_id,
                                                                  service_price_id=service_price_id,
                                                                  service_plan_id=service_plan_id,
                                                                  hw_id=pk)
        return render(request, 'admin/frontend/special_offers/servies/editorview_hardware_price.html',
                      {'hw': hw,
                       'hw_id':pk,
                       'special_offers_id':special_offers_id,
                       'service_plan_id':service_plan_id,
                       'service_price_id':service_price_id,
                       'spOffershw':spOffershw
                       })
    elif request.method == 'POST':
        try:
            if SpecialOffersPlanswithHardwareRates.objects.filter(special_offers_id=special_offers_id,
                                                                  service_price_id=service_price_id,
                                                                  service_plan_id=service_plan_id,
                                                                  hw_id=pk).exists():
                
               spOffershw =  SpecialOffersPlanswithHardwareRates.objects.get(special_offers_id=special_offers_id,service_price_id=service_price_id,service_plan_id=service_plan_id,hw_id=pk)
               spOffershw.device_buy=request.POST['device_buy']
               spOffershw.device_rental=request.POST['device_rental']
               spOffershw.montly_rent=request.POST['montly_rent']
               spOffershw.hw_qty=request.POST['hw_qty']
               spOffershw.offer_price=request.POST['offer_price']
               spOffershw.save()
               
            messages.add_message(request, messages.SUCCESS,  'Special Offers Hardware according to service plan updated successfully')
            return HttpResponseRedirect(reverse('editorview_special_offers_services_plan_hardware_offer_price',kwargs={'pk':pk,'special_offers_id':special_offers_id,'service_plan_id':service_plan_id,'service_price_id':service_price_id}))
        except Exception as e:
            messages.add_message(request, messages.ERROR, e)
            return HttpResponseRedirect(reverse('editorview_special_offers_services_plan_hardware_offer_price',kwargs={'pk':pk,'special_offers_id':special_offers_id,'service_plan_id':service_plan_id,'service_price_id':service_price_id}))

# @login_required(login_url="/admin")
# @user_passes_test(my_check,login_url='/admin')
# def special_offers_settings_manage_service_price_edit(request, pk,category_id):
#        if request.method == 'GET':
#             servies_category = ManageServicesPriceCategory.objects.values('id', 'service_category_name', 'status').filter(pk=category_id)
#             servies = ManageServicePrice.objects.values('id', 'service_name','service_price','service_category_id','status','service_desc').filter(pk=pk)
#             return render(request, 'admin/frontend/special_offers/servies/services_edit.html',
#                           {'servies': servies,'servies_category':servies_category,'category_id':category_id})
#        elif request.method == 'POST':
#             form = ManageServicesPriceForm(request.POST)
#             try:
#                 data = ManageServicePrice.objects.get(pk=pk)
#                 if form.is_valid():
#                     data.service_category_id = form['service_category'].data
#                     data.service_name = form['service_name'].data
#                     data.service_price = form['service_price'].data
#                     data.service_desc = form['service_desc'].data
#                     data.status = form['status'].data
#                     data.save()
#                     messages.add_message(request, messages.SUCCESS, 'Service Edited successfully')
#                     return HttpResponseRedirect(reverse('special_offers_settings_manage_service_price_edit', kwargs={'pk':pk,'category_id':category_id}))
#                 else:
#                     messages.add_message(request, messages.ERROR, form.errors)
#                     return HttpResponseRedirect(reverse('special_offers_settings_manage_service_price_edit', kwargs={'pk': pk,'category_id':category_id}))
#
#             except ManageServicePrice.DoesNotExist:
#                 data = None
#                 messages.add_message(request, messages.ERROR, 'Error')
#                 return HttpResponseRedirect(reverse('special_offers_settings_manage_service_price_edit', kwargs={'pk': pk,'category_id':category_id}))
#
# #delete
# @login_required(login_url="/admin")
# @user_passes_test(my_check,login_url='/admin')
# def special_offers_settings_manage_service_price_delete(request,pk):
#     if request.method == 'GET':
#         if ManageServicePrice.objects.filter(pk=pk).exists():
#             ManageServicePrice.objects.filter(pk=pk).delete()
#             messages.add_message(request, messages.SUCCESS, 'Service Deleted successfully')
#             return HttpResponseRedirect(reverse('special_offers'))
#         else:
#             messages.add_message(request, messages.ERROR, 'Error Occure')
#             return HttpResponseRedirect(reverse('special_offers'))
#
# @login_required(login_url="/admin")
# @user_passes_test(my_check,login_url='/admin')
# def special_offers_settings_manage_service_price_value_update(request):
#     if request.is_ajax():
#         price = request.POST['service_price']
#         pk = request.POST['pk']
#         if ManageServicePrice.objects.filter(pk=pk).exists():
#             try :
#                 data = ManageServicePrice.objects.get(pk=pk)
#                 data.service_price = price
#                 data.save()
#                 msg = price
#                 return HttpResponse(json.dumps({"data": msg}), content_type="application/json")
#
#             except ManageServicePrice.DoesNotExist:
#                 msg = 'Your Password Be changed'
#                 return HttpResponse(json.dumps({"data": msg}), content_type="application/json")
#
#         else:
#             msg = 'New password and confirm password should be matched'
#             return HttpResponse(json.dumps({"data": msg}), content_type="application/json")


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def special_offers_doc_add(request,id):
    if request.method == 'GET':
        return render(request, 'admin/frontend/special_offers/servies/add_doc.html',{'id':id})
    elif request.method =='POST':
        forms = SpecialOffersDocForm(request.POST,request.FILES)
        if forms.is_valid():
            forms.save()
            messages.add_message(request, messages.SUCCESS, 'Document Uploaded successfully')
            return HttpResponseRedirect(reverse('special_offers_doc_add',kwargs={'id':id}))
        else:
            messages.add_message(request, messages.ERROR, forms.errors)
            return HttpResponseRedirect(reverse('special_offers_doc_add',kwargs={'id':id}))

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def special_offers_doc_view(request, id):
    if request.method == 'GET':
        data = Specialoffersdoc.objects.values('id','special_offers_doc_name','special_offers_doc','special_offers_id','created_at','status').filter(special_offers_id=id)
        return render(request, 'admin/frontend/special_offers/servies/view_doc.html',
                      {'id': id,'data':data})


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def special_offers_doc_delete(request,id,special_offers_id):
    if request.method == 'GET':
        if Specialoffersdoc.objects.filter(id=id).exists():
            Specialoffersdoc.objects.filter(id=id).delete()
        messages.add_message(request, messages.SUCCESS, 'Document Deleted successfully')
        return HttpResponseRedirect(reverse('special_offers_doc_view', kwargs={'id': special_offers_id}))
    else:
        messages.add_message(request, messages.ERROR, forms.errors)
        return HttpResponseRedirect(reverse('special_offers_doc_view', kwargs={'id': special_offers_id}))


# DOC status change

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def special_offers_doc_status_change(request):
    if request.is_ajax:
        id = request.POST['id']
        if Specialoffersdoc.objects.filter(pk=id).exists():
            msc = Specialoffersdoc.objects.values('id', 'status').filter(pk=id)
            if msc[0]['status'] == 'active':
                data = Specialoffersdoc.objects.get(pk=id)
                data.status = 'inactive'
                data.save()
                msg = 'Status Updated successfully as ' + ' ' + data.status + '. Now you can not show download button in front end section.'
                msc = Specialoffersdoc.objects.values('id', 'status').filter(pk=id)
                data = render_to_string('admin/settings/manage_service_price/servies/list.html', {'msc': msc})
                return HttpResponse(json.dumps({"data": data, "msg": msg}), content_type="application/json")
            else:
                data = Specialoffersdoc.objects.get(pk=id)
                data.status = 'active'
                data.save()
                msg = 'Status Updated successfully as ' + ' ' + data.status + '. Now you can show download button in front end section.'
                msc = Specialoffersdoc.objects.values('id', 'status').filter(pk=id)
                data = render_to_string('admin/settings/manage_service_price/servies/list.html', {'msc': msc})
                return HttpResponse(json.dumps({"data": data, "msg": msg}), content_type="application/json")
        
        else:
            msg = 'Warning ! Your documents does not exists.'
            return HttpResponse(json.dumps({"data": msg}), content_type="application/json")
        