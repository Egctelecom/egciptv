from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.template.loader import render_to_string
from adminsidecustomer.forms import CutomerAttachmentform, CustomerTicketsform
from adminsidecustomer.models import CutomerAttachmentMap,AccountAddressCustomer
from adminsideserviceprovider.models import CustomerTicketsCategoriesMap, TicketsCategories, ServiceProviderPlan, \
    ServiceProvider

from adminsideserviceprovider.models import CustomerServiceContract,CustomerWithService,ServicePlanWithHardware,Hardware,ServiceProviderPlan,ServiceProviderCityMap,TicketsCategoryWithServiceProvider
from django.contrib.auth.decorators import user_passes_test
import  json
def my_check(user):
    return user.is_superuser == True

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def add_upload_documents(request,id):
    if request.method == 'GET':
        return render(request,'admin/customer/add_upload_documents.html',{'id':id})
    if request.method == 'POST':
        form =  CutomerAttachmentform(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Document Update successfully')
            return HttpResponseRedirect(reverse('upload_documents', kwargs={'id': id}))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('upload_documents', kwargs={'id': id}))

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def delete_upload_documents(request,id):
    if request.method == 'GET':
        cid = request.session['customer']
        if CutomerAttachmentMap.objects.filter(pk=id).exists():
            CutomerAttachmentMap.objects.filter(pk=id).delete()
            messages.add_message(request, messages.SUCCESS, 'Document delete successfully')
            return HttpResponseRedirect(reverse('customer_details', kwargs={'id': cid}))
        else:
            messages.add_message(request, messages.ERROR, 'No data found')
            return HttpResponseRedirect(reverse('customer_details', kwargs={'id': cid}))

#======================================================================================= Create Ticket for user ===========================================================================================================================#

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def create_tickets(request,id):
    if request.method == 'GET':
        customer_plan_data = CustomerServiceContract.objects.values('id',
                                                                    'user_id',
                                                                    'customerwithservice', 'service_plan_hardware'
                                                                    ).filter(user_id=id, type='New')
        
        
        ticket_category = TicketsCategories.objects.values('id','category_title')
        uploaduser = request.user.id
        providers = ServiceProvider.objects.all()
        
        return render(request, 'admin/customer/create_tickets.html', {'id': id,
                                                                      'customer_plan_data': customer_plan_data,
                                                                      'ticket_category': ticket_category,
                                                                      'uploaduser': uploaduser, 'providers': providers})
    if request.method == 'POST':
        # dt = CustomerServiceContract.objects.values('id',
        #                                          'user_id',
        #                                          'customerwithservice','service_plan_hardware','payment_status'
        #                                          ).filter(user_id=id, type='New')
        # for dtt in dt:
        #  if dtt['payment_status'] == 'Pending':
        #      messages.add_message(request, messages.SUCCESS, 'Contract in pending')
        #      return HttpResponseRedirect(reverse('create_tickets', kwargs={'id': id}))
        #  else:
        #      if CustomerTicketsCategoriesMap.objects.filter(service_plan_hardware_id=request.POST['service_plan_hardware']).exists():
        #          data = CustomerTicketsCategoriesMap.objects.values('id','working_status').filter(service_plan_hardware_id=request.POST['service_plan_hardware'])
        #          messages.add_message(request, messages.SUCCESS, 'Ticket already created for this issue now it '+' ' +data[0]['working_status']+' '+'mode')
        #          print('service plan h/w'+request.session['service_plan_hardware'])
        #          print('service provider id'+request.session['service_provider_id'])
        #          return HttpResponseRedirect(reverse('create_tickets', kwargs={'id': id}))
        #      else:
        form = CustomerTicketsform(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Ticket created  successfully')
            return HttpResponseRedirect(reverse('create_tickets', kwargs={'id': id}))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('create_tickets', kwargs={'id': id}))


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def edit_tickets(request,id):
    if request.method == 'GET':
        data = CustomerTicketsCategoriesMap.objects.values('id',
                                                           'customer_id','customer_id__first_name',
                                                           'customer_id','customer_id__last_name',
                                                           'customer_id','customer_id__account_id',
                                                           'customer_id',
                                                           'ticketCategory_id',
                                                           'ticketCategory_id__category_title',
                                                           # 'service_provider_id',
                                                           # 'service_provider_id__service_provider_name',
                                                           # 'service_plan_hardware_id',
                                                           'subject',
                                                           'threads',
                                                           'category',
                                                           'priority',
                                                           'working_status',
                                                           'updatedby_id',
                                                           'updatedby_id__username',
                                                           'created_at',
                                                           'updated_at').filter(pk=id)
        return render(request, 'admin/customer/edit_tickets.html', {'id': id,'data':data})
    if request.method == 'POST':
        data = CustomerTicketsCategoriesMap.objects.get(pk=id)
        form = CustomerTicketsform(request.POST)
        if form.is_valid():
            data.subject = form['subject'].data
            data.threads = form['threads'].data
            data.category = form['category'].data
            data.priority = form['priority'].data
            data.save()
            messages.add_message(request, messages.SUCCESS, 'Ticket Update  successfully')
            return HttpResponseRedirect(reverse('edit_tickets', kwargs={'id': id}))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('edit_tickets', kwargs={'id': id}))


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def delete_tickets(request,id):
    if request.method == 'GET':
        cid = request.session['customer']
        if CustomerTicketsCategoriesMap.objects.filter(pk=id).exists():
            CustomerTicketsCategoriesMap.objects.filter(pk=id).delete()
            messages.add_message(request, messages.SUCCESS, 'Ticket delete  successfully')
            return HttpResponseRedirect(reverse('customer_details', kwargs={'id': cid}))
        else:
            messages.add_message(request, messages.ERROR, 'No data found')
            return HttpResponseRedirect(reverse('customer_details', kwargs={'id': cid}))



#======================================================================================= Get Service Plan With Provider ===========================================================================================================================#

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def get_service_with_ticket(request):
    if request.is_ajax():
        ticketCategory = request.POST['ticketCategory']
        user_id = request.POST['user_id']
        
        customer_city = AccountAddressCustomer.objects.values('id', 'city_id').filter(user_id=user_id)
        
        service_provider = ServiceProviderCityMap.objects.values('id', 'service_provider_id').filter(
            city_id=customer_city[0]['city_id'])
        
        ticket_service_provider = TicketsCategoryWithServiceProvider.objects.values('id','service_provider_id').filter(ticket_category_id=ticketCategory)
        
        service_provider_array=[]
        for ser  in service_provider:
            service_provider_array.append(ser['service_provider_id'])
        
        ticket_service_provider_array=[]
        for tser in ticket_service_provider:
            ticket_service_provider_array.append(tser['service_provider_id'])
        
        toresult = []
        for element in service_provider_array:
            if element in ticket_service_provider_array:
                toresult.append(element)
        
        customerServiceContracts = CustomerServiceContract.objects.values('id', 'customerwithservice').filter(user_id=user_id)
        contract=[]
        for c in customerServiceContracts:
            customerServiceContract = c['customerwithservice']
            customerServiceContract =  customerServiceContract.replace('"[','')
            customerServiceContract =  customerServiceContract.replace(']"','')
            contract.append(customerServiceContract)
        
        sub_result=[]
        for element in contract:
            service = ServiceProviderPlan.objects.values('service_provider_id','id').filter(pk=element)
            sub_result.append(service[0]['service_provider_id'])
        
        result = []
        for element in toresult:
            # if element in sub_result:
            result.append(element)
        request.session['service_provider_id'] = json.dumps(result)
        
        data = render_to_string('admin/customer/ticket/list.html', {'result':result})
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def get_service_hw_with_ticket(request):
    if request.is_ajax():
        service_providerID = request.POST['service_provider']
        user_id = request.POST['user_id']
        
        
        service_provider_plan = ServiceProviderPlan.objects.values('id').filter(service_provider_id=service_providerID)
        
        
        hwlistarray=[]
        for sp in  service_provider_plan:
            sw = ServicePlanWithHardware.objects.values('hw_id').filter(service_plan_id=sp['id'])
            for sp in sw:
                hwlistarray.append(sp['hw_id'])
        
        customerServiceContractshw = CustomerServiceContract.objects.values('id', 'service_plan_hardware').filter(user_id=user_id)
        
        contracthw = []
        
        for c in customerServiceContractshw:
            customerServiceContracthw = c['service_plan_hardware']
            customerServiceContracthw = customerServiceContracthw.replace('[', '')
            customerServiceContracthw = customerServiceContracthw.replace(']', '')
            contracthw.append(customerServiceContracthw)
        
        sub_result = []
        for element in contracthw:
            if element != '':
                service = ServicePlanWithHardware.objects.values('hw_id', 'id').filter(pk=element)
                sub_result.append(service[0]['hw_id'])
        
        result = []
        for element in hwlistarray:
            if element in sub_result:
                result.append(element)
        
        request.session['service_plan_hardware'] = json.dumps(result)
        
        data = render_to_string('admin/customer/ticket/hwlist.html', {'result':result})
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")


