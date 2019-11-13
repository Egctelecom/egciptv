from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
import http.client
import json
import requests
from django.urls import reverse
from adminsidecustomer.models import Sales_tax,Province
from adminsidecustomer.forms import SalesTaxform
from django.contrib import messages
from django.http import HttpResponseRedirect


def my_check(user):
    return user.is_superuser == True


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def sales_tax_details(request):
    if request.method == 'GET':
        salestax = Sales_tax.objects.values('id',
                                            'province_id',
                                            'province_id__province_name',
                                            'tax_name',
                                            'abbreviation',
                                            'description',
                                            'tax_number',
                                            'is_tax_number_show',
                                            'is_fedral_tax',
                                            'is_provisional_tax',
                                            'tax_rate')
        return render(request, 'admin/sales_tax/index.html',{'salestaxs':salestax})


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def add_sales_tax(request):
    if request.method == 'GET':
        province = Province.objects.values('province_name', 'id')
        return render(request, 'admin/sales_tax/add.html',{'province':province})
    elif request.method == 'POST':
        form = SalesTaxform(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Sales Tax Added Successfully')
            return HttpResponseRedirect(reverse('add_sales_tax'))
        else:
            messages.add_message(request, messages.SUCCESS, form.errors)
            return HttpResponseRedirect(reverse('add_sales_tax'))

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def edit_sales_tax(request,pk):
    if request.method == 'GET':
        province = Province.objects.values('province_name', 'id')
        salestax = Sales_tax.objects.values('id',
                                            'province_id',
                                            'province_id__province_name',
                                            'tax_name',
                                            'abbreviation',
                                            'description',
                                            'tax_number',
                                            'is_tax_number_show',
                                            'is_fedral_tax',
                                            'is_provisional_tax',
                                            'tax_rate'
                                            ).filter(pk=pk)
        return render(request, 'admin/sales_tax/edit.html',{'province':province,'salestax':salestax})
    elif request.method == 'POST':
        data = Sales_tax.objects.get(pk=pk)
        form = SalesTaxform(request.POST)
        if form.is_valid():
            data.tax_name = form['tax_name'].data
            data.abbreviation = form['abbreviation'].data
            data.description = form['description'].data
            data.tax_number = form['tax_number'].data
            data.is_tax_number_show = form['is_tax_number_show'].data
            data.is_fedral_tax = form['is_fedral_tax'].data
            data.is_provisional_tax = form['is_provisional_tax'].data
            data.tax_rate = form['tax_rate'].data
            data.save()
            messages.add_message(request, messages.SUCCESS, 'Sales Tax Added Successfully')
            return HttpResponseRedirect(reverse('edit_sales_tax', kwargs={'pk': pk}))
        else:
            messages.add_message(request, messages.SUCCESS, form.errors)
            return HttpResponseRedirect(reverse('edit_sales_tax', kwargs={'pk': pk}))

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def delete_sales_tax(request,pk):
    if Sales_tax.objects.filter(pk=pk).exists():
        Sales_tax.objects.filter(pk=pk).delete()
        messages.add_message(request, messages.SUCCESS, 'Delete Successfully')
        return HttpResponseRedirect(reverse('sales_tax'))
