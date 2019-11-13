from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from crmadmin.forms import Serviceform
from crmadmin.models import Services

from django.contrib.auth.decorators import user_passes_test

def my_check(user):
    return user.is_superuser == True

@user_passes_test(my_check,login_url='/admin')
def services_index(request):
    if request.method == 'GET':
        services = Services.objects.values('id','title','price')
        return render(request, 'admin/services/index.html',{'services':services})

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def services_add(request):
    if request.method == 'GET':
        return render(request, 'admin/services/add.html')
    if request.method == 'POST':
        form = Serviceform(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Services Added')
            return HttpResponseRedirect(reverse('services_add'))
        else:
            messages.add_message(request, messages.SUCCESS, 'Services Not Added')
            return HttpResponseRedirect(reverse('services_add'))

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def services_edit(request,pk):
    if request.method == 'GET':
        services = Services.objects.filter(pk=pk).values('id', 'title', 'price')
        return render(request, 'admin/services/edit.html',{'services':services})
    elif request.method == 'POST':
        form = Serviceform(request.POST)
        data = Services.objects.get(pk=pk)
        if form.is_valid():
            if form.is_valid():
                data.title = form['title'].data
                data.price = form['price'].data
                data.save()
            messages.add_message(request, messages.SUCCESS, 'Services Update')
            return HttpResponseRedirect(reverse('services_edit',kwargs={'pk':pk}))
        else:
            messages.add_message(request, messages.SUCCESS, 'Services Not Update')
            return HttpResponseRedirect(reverse('services_edit',kwargs={'pk':pk}))

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def services_delete(request,pk):
    if request.method == 'GET':
        if Services.objects.filter(pk=pk).exists():
            Services.objects.filter(pk=pk).delete()
            messages.add_message(request, messages.SUCCESS, 'Services Delete successfully')
            return HttpResponseRedirect(reverse('services_index'))
        else:
            messages.add_message(request, messages.SUCCESS, 'Services Delete not deleted')
            return HttpResponseRedirect(reverse('services_index'))
