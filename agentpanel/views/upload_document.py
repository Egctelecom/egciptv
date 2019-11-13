from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from agentpanel.models import Agent

from adminsidecustomer.forms import CutomerAttachmentform, CustomerTicketsform
from adminsidecustomer.models import CutomerAttachmentMap
from adminsideserviceprovider.models import CustomerTicketsCategoriesMap

from django.contrib.auth.decorators import user_passes_test

def my_check(user):
    if Agent.objects.filter(user_id=user.id).exists():
        if user.is_superuser == False:
            data = True
            return data

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def add_upload_documents(request,id):
    if request.method == 'GET':
        return render(request,'agent/customer/add_upload_documents.html',{'id':id})
    if request.method == 'POST':
        form =  CutomerAttachmentform(request.POST,request.FILES)
        if form.is_valid():
           form.save()
           messages.add_message(request, messages.SUCCESS, 'Document Update successfully')
           return HttpResponseRedirect(reverse('agent_upload_documents', kwargs={'id': id}))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('agent_upload_documents', kwargs={'id': id}))

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def delete_upload_documents(request,id):
    if request.method == 'GET':
        cid = request.session['customer']
        if CutomerAttachmentMap.objects.filter(pk=id).exists():
            CutomerAttachmentMap.objects.filter(pk=id).delete()
            messages.add_message(request, messages.SUCCESS, 'Document delete successfully')
            return HttpResponseRedirect(reverse('agent_customer_details', kwargs={'id': cid}))
        else:
            messages.add_message(request, messages.ERROR, 'No data found')
            return HttpResponseRedirect(reverse('agent_customer_details', kwargs={'id': cid}))

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def create_tickets(request,id):
    if request.method == 'GET':
        return render(request, 'agent/customer/create_tickets.html', {'id': id})
    if request.method == 'POST':
        form = CustomerTicketsform(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Ticket created  successfully')
            return HttpResponseRedirect(reverse('agent_create_tickets', kwargs={'id': id}))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('agent_create_tickets', kwargs={'id': id}))

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def edit_tickets(request,id):
    if request.method == 'GET':
        data = CustomerTicketsCategoriesMap.objects.values('id','customer_id','subject','threads','category','priority').filter(pk=id)
        return render(request, 'agent/customer/edit_tickets.html', {'id': id,'data':data})
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
            return HttpResponseRedirect(reverse('agent_edit_tickets', kwargs={'id': id}))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('agent_edit_tickets', kwargs={'id': id}))


@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def delete_tickets(request,id):
    if request.method == 'GET':
        cid = request.session['customer']
        if CustomerTicketsCategoriesMap.objects.filter(pk=id).exists():
            CustomerTicketsCategoriesMap.objects.filter(pk=id).delete()
            messages.add_message(request, messages.SUCCESS, 'Ticket delete  successfully')
            return HttpResponseRedirect(reverse('agent_customer_details', kwargs={'id': cid}))
        else:
            messages.add_message(request, messages.ERROR, 'No data found')
            return HttpResponseRedirect(reverse('agent_customer_details', kwargs={'id': cid}))