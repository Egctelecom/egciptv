from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from adminsidecustomer.models import Country,Province,City
from setcountryprovincecity.forms import Setcountryform,Setprovinceform,Setcityform
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

def my_check(user):
    return user.is_superuser == True

#============================================================================== Country ==========================================================================================================#

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def get_country(request):
    if request.method == 'GET':
	    country_list = Country.objects.values('id','country_name')
	    return render(request, 'admin/countrystatecity/country/index.html',
	                  {'country_list': country_list})


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def add_country(request):
	if request.method == 'GET':
		return render(request, 'admin/countrystatecity/country/add.html')
	elif request.method == 'POST':
		form = Setcountryform(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Country Add Successfully')
			return HttpResponseRedirect(reverse('add_country'))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('add_country'))

			
			
@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def edit_country(request,pk):
	if request.method == 'GET':
		country_list = Country.objects.values('id', 'country_name')
		return render(request, 'admin/countrystatecity/country/edit.html',{'country_list':country_list})
	elif request.method == 'POST':
		data = Country.objects.get(pk=pk)
		form = Setcountryform(request.POST)
		if form.is_valid():
			data.country_name = form['country_name'].data
			data.save()
			messages.add_message(request, messages.SUCCESS, 'Country Edit Successfully')
			return HttpResponseRedirect(reverse('edit_country',kwargs={'pk': pk}))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('edit_country',kwargs={'pk': pk}))


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def delete_country(request,pk):
	if Country.objects.filter(pk=pk).exists():
		Country.objects.filter(pk=pk).delete()
		return HttpResponseRedirect(reverse('get_country'))
	
	
#============================================================================== Province ==========================================================================================================#

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def get_province(request):
	if request.method == 'GET':
		province_list = Province.objects.values('id','country_id', 'country_id__country_name','province_name')
		country_list = Country.objects.values('id', 'country_name')

		return render(request, 'admin/countrystatecity/province/index.html',
		              {'province_list': province_list,'country_list':country_list})

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def add_province(request):
	if request.method == 'GET':
		country_list = Country.objects.values('id', 'country_name')
		return render(request, 'admin/countrystatecity/province/add.html',{'country_list':country_list})
	elif request.method == 'POST':
		form = Setprovinceform(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Province Add Successfully')
			return HttpResponseRedirect(reverse('add_province'))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('add_province'))

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def edit_province(request,pk):
	if request.method == 'GET':
		province_list = Province.objects.values('id','country_id', 'country_id__country_name','province_name').filter(pk=pk)
		return render(request, 'admin/countrystatecity/province/edit.html', {'province_list': province_list})
	elif request.method == 'POST':
		data = Province.objects.get(pk=pk)
		form = Setprovinceform(request.POST)
		if form.is_valid():
			data.province_name = form['province_name'].data
			data.save()
			messages.add_message(request, messages.SUCCESS, 'Province Edit Successfully')
			return HttpResponseRedirect(reverse('edit_province', kwargs={'pk': pk}))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('edit_province', kwargs={'pk': pk}))

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def delete_province(request,pk):
	if Province.objects.filter(pk=pk).exists():
		Province.objects.filter(pk=pk).delete()
		return HttpResponseRedirect(reverse('get_province'))
		
#============================================================================== City ==========================================================================================================#

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def get_city(request,pk):
	if request.method == 'GET':
		city_list = City.objects.values('id', 'city_name','province_id','province_id__province_name').filter(province_id=pk)
		return render(request, 'admin/countrystatecity/city/index.html',
		              {'city_list': city_list,'province_id':pk})

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def add_city(request,pk):
	if request.method == 'GET':
		province_list = Province.objects.values('id', 'province_name')
		provinceID = Province.objects.values('id', 'province_name').filter(pk=pk)
		return render(request, 'admin/countrystatecity/city/add.html', {'province_list': province_list,'provinceID':provinceID})
	elif request.method == 'POST':
		form = Setcityform(request.POST)
		if form.is_valid():
			City.objects.create(province_id_id=pk,city_name=request.POST['city_name'])
			messages.add_message(request, messages.SUCCESS, 'City Add Successfully')
			return HttpResponseRedirect(reverse('add_city',kwargs={'pk': pk}))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('add_city',kwargs={'pk': pk}))

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def edit_city(request, pk):
	if request.method == 'GET':
		province_list = Province.objects.values('id', 'province_name')
		city_list = City.objects.values('id', 'city_name', 'province_id').filter(pk=pk)
		return render(request, 'admin/countrystatecity/city/edit.html', {'province_list': province_list,'city_list':city_list})
	elif request.method == 'POST':
		data = City.objects.get(pk=pk)
		form = Setcityform(request.POST)
		if form.is_valid():
			data.city_name = form['city_name'].data
			data.save()
			messages.add_message(request, messages.SUCCESS, 'City Edit Successfully')
			return HttpResponseRedirect(reverse('edit_city', kwargs={'pk': pk}))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('edit_city', kwargs={'pk': pk}))

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def delete_city(request, pk):
	if City.objects.filter(pk=pk).exists():
		City.objects.filter(pk=pk).delete()
		return HttpResponseRedirect(reverse('get_city'))
