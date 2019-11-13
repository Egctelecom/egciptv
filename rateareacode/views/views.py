from django.shortcuts import render
from rateareacode.models import Ratewithareacode
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from adminsidecustomer.models import Country,Province
from rateareacode.forms import RatewithareacodeForm
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect,JsonResponse


def my_check(user):
	return user.is_superuser == True


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def index(request):
	if request.method == 'GET':
		rate_with_area = Ratewithareacode.objects.values('id','country_id__country_name', 'province_id__province_name',
		                                                 'area_code', 'rate', 'status').order_by('-created_at')
		return render(request, 'admin/areacode_with_rate/index.html', {'rate_with_area': rate_with_area})


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def add(request):
	if request.method == 'GET':
		country = Country.objects.values('id', 'country_name')
		return render(request, 'admin/areacode_with_rate/add.html', {'country_list': country})
	elif request.method == 'POST':
		form = RatewithareacodeForm(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Area Code DEtails successfully add')
			return HttpResponseRedirect(reverse('areacode_with_rate_add'))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('areacode_with_rate_add'))


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def edit(request,id):
	if request.method == 'GET':
		country = Country.objects.values('id', 'country_name')
		province = Province.objects.values('id', 'province_name')
		rate_with_area = Ratewithareacode.objects.values('id','country_id__country_name', 'province_id__province_name','country_id','province_id',
		                                                 'area_code', 'rate', 'status').filter(pk=id)
		return render(request, 'admin/areacode_with_rate/edit.html', {'country_list': country,'rate_with_area':rate_with_area,'province_list':province})
	elif request.method == 'POST':
		data = Ratewithareacode.objects.get(pk=id)
		form = RatewithareacodeForm(request.POST)
		if form.is_valid():
			data.area_code = form['area_code'].data
			data.rate = form['rate'].data
			data.status = form['status'].data
			data.save()
			messages.add_message(request, messages.SUCCESS, 'Area Code Details successfully updated')
			return HttpResponseRedirect(reverse('areacode_with_rate_edit',kwargs={'id': id}))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('areacode_with_rate_edit',kwargs={'id': id}))
		
@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def status_changes(request):
  if request.is_ajax():
       id = request.POST["id"]
       print(id)
       data = Ratewithareacode.objects.get(pk=id)
       if  data.status == 'False':
           data.status = 'True'
           data.save()
           response_data = {}
           response_data['result'] = 'checked'
           return JsonResponse(response_data, safe=False)

       else:
           data.status = 'False'
           data.save()
           response_data = {}
           response_data['result'] = 'unchecked'
           return JsonResponse(response_data, safe=False)
	  

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def delete(request,id):
	if request.method == 'GET':
		if Ratewithareacode.objects.filter(pk=id).exists():
			Ratewithareacode.objects.filter(pk=id).delete()
			return HttpResponseRedirect(reverse('area_rate'))

