from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
import requests
import json

from django.views.decorators.csrf import csrf_exempt

from sitefrontendbyadmin.models import SpecialoffersUnderCategory,SpecialoffersSubParentCategory,SpecialoffersParentCategory,SpecialOffers
from crmadmin.forms import SpecialoffersParentCategoryForm,SpecialoffersSubParentCategoryForm,SpecialoffersUnderCategoryForm
from adminsidecustomer.models import Province ,City

def my_check(user):
	return user.is_superuser == True


# ======================================================================= Parent Category ==========================================================================================================================


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def special_offers_parent_category_list(request):
	if request.method == 'GET':
		special_offers_list = SpecialoffersParentCategory.objects.values('id', 'special_offers_parent_category_name','status')
		return render(request, 'admin/frontend/special_offers/services_category/parent/index.html', {'special_offers_list': special_offers_list})


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def special_offers_parent_category_add(request):
	if request.method == 'GET':
		category_list = SpecialoffersParentCategory.objects.values('id', 'special_offers_parent_category_name','desc','status')
		return render(request, 'admin/frontend/special_offers/services_category/parent/add.html', {'category_list': category_list})
	
	elif request.method == 'POST':
		form = SpecialoffersParentCategoryForm(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Special Offers Section Parent Category Added successfully')
			return HttpResponseRedirect(reverse('special_offers_parent_category_add'))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('special_offers_parent_category_add'))


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def special_offers_parent_category_edit(request,id):
	if request.method == 'GET':
		for_edited_menu = SpecialoffersParentCategory.objects.values('id', 'special_offers_parent_category_name','desc','status').filter(pk=id)
		
		return render(request, 'admin/frontend/special_offers/services_category/parent/edit.html', {'for_edited_menu': for_edited_menu})
	
	elif request.method == 'POST':
		data = SpecialoffersParentCategory.objects.get(pk=id)
		form = SpecialoffersParentCategoryForm(request.POST)
		if form.is_valid():
			data.special_offers_parent_category_name = form['special_offers_parent_category_name'].data
			data.desc = form['desc'].data
			data.status = form['status'].data
			data.save()
			messages.add_message(request, messages.SUCCESS, 'Special offers Section Parent Category Updated successfully')
			return HttpResponseRedirect(reverse('special_offers_parent_category_edit', kwargs={'id': id}))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('special_offers_parent_category_edit', kwargs={'id': id}))


# ======================================================================= Parent Sub Category ==========================================================================================================================

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def special_offers_parent_sub_category_list(request):
	if request.method == 'GET':
		special_offers_list = SpecialoffersSubParentCategory.objects.values('id', 'special_offers_sub_parent_category_name',
		                                                                    'special_offers_parent_category_id__special_offers_parent_category_name','desc','status')
		return render(request, 'admin/frontend/special_offers/services_category/subparent/index.html', {'special_offers_list': special_offers_list})


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def special_offers_parent_sub_category_add(request):
	if request.method == 'GET':
		category_list = SpecialoffersSubParentCategory.objects.values('id', 'special_offers_sub_parent_category_name','desc','status')
		parent_category_list = SpecialoffersParentCategory.objects.values('id', 'special_offers_parent_category_name','desc','status')
		return render(request, 'admin/frontend/special_offers/services_category/subparent/add.html',
		              {'category_list': category_list, 'parent_category_list': parent_category_list})
	
	elif request.method == 'POST':
		form = SpecialoffersSubParentCategoryForm(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Special Offers Section Sub Parent Category Added successfully')
			return HttpResponseRedirect(reverse('special_offers_parent_sub_category_add'))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('special_offers_parent_sub_category_add'))


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def special_offers_sub_parent_category_edit(request, id):
	if request.method == 'GET':
		
		category_list = SpecialoffersParentCategory.objects.values('id',
		                                                           'special_offers_parent_category_name',
		                                                           'desc',
		                                                           'status')
		
		for_edited_menu = SpecialoffersSubParentCategory.objects.values('id',
		                                                                'special_offers_parent_category_id',
		                                                                'special_offers_sub_parent_category_name',
		                                                                'desc',
		                                                                'status').filter(pk=id)
		
		
		
		
		return render(request, 'admin/frontend/special_offers/services_category/subparent/edit.html',
		              {'for_edited_menu': for_edited_menu, 'category_list': category_list})
	
	elif request.method == 'POST':
		data = SpecialoffersSubParentCategory.objects.get(pk=id)
		form = SpecialoffersSubParentCategoryForm(request.POST)
		if form.is_valid():
			data.special_offers_sub_parent_category_name = form['special_offers_sub_parent_category_name'].data
			data.desc = form['desc'].data
			data.status = form['status'].data
			data.save()
			messages.add_message(request, messages.SUCCESS, 'Special Offers Section Sub Parent Category Updated successfully')
			return HttpResponseRedirect(reverse('special_offers_parent_sub_category_edit', kwargs={'id': id}))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('special_offers_parent_sub_category_edit', kwargs={'id': id}))


# ======================================================================= Category ==========================================================================================================================
@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def special_offers_category_list(request):
	if request.method == 'GET':
		special_offers_list = SpecialoffersUnderCategory.objects.values('id',
		                                                                'special_offers_id',
		                                                                'special_offers_parent_category_id',
		                                                                'telecom_name',
		                                                                'telecom_logo',
		                                                                'special_offers_sub_parent_category_id',
		                                                                'special_offers_combo_name',
		                                                                'special_offers_type_name',
		                                                                'city_id',
		                                                                'city_id__city_name',
		                                                                'province_id',
		                                                                'province_id__province_name',
		                                                                'special_offers_parent_category_id__special_offers_parent_category_name',
		                                                                'special_offers_sub_parent_category_id__special_offers_sub_parent_category_name',
		                                                                'status')
		return render(request, 'admin/frontend/special_offers/services_category/category/index.html', {'special_offers_list': special_offers_list})

# Add Special Offers Under Category

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def special_offers_category_add(request):
	if request.method == 'GET':
		special_offers_parent_category_list = SpecialoffersParentCategory.objects.values('id', 'special_offers_parent_category_name')
		special_offers_list = SpecialOffers.objects.values('id')
		provinces = Province.objects.values('id','province_name','country_id__id','country_id__country_name')
		city = City.objects.values('id','city_name','province_id__province_name','province_id__id')
		return render(request, 'admin/frontend/special_offers/services_category/category/add.html',
		              {'special_offers_parent_category_list': special_offers_parent_category_list,
		               'special_offers_list': special_offers_list,
		               'provinces':provinces
		               })
	
	elif request.method == 'POST':
		if SpecialoffersUnderCategory.objects.filter(special_offers_id=request.POST['special_offers'],
		                                             city_id=request.POST['city'],
		                                             province_id=request.POST['province']).exists():
			
			messages.add_message(request, messages.SUCCESS, 'This Special offers already added under Parent and Sub Parent Category on this city and province. Please Try another Special Offers.')
			return HttpResponseRedirect(reverse('special_offers_category_add'))
		else:
			form = SpecialoffersUnderCategoryForm(request.POST,request.FILES)
			if form.is_valid():
				form.save()
				messages.add_message(request, messages.SUCCESS, 'Special Offers Section Category Added successfully')
				return HttpResponseRedirect(reverse('special_offers_category_add'))
			else:
				messages.add_message(request, messages.ERROR, form.errors)
				return HttpResponseRedirect(reverse('special_offers_category_add'))

# Edit Special Offers Under Category

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def special_offers_category_edit(request,id):
	if request.method == 'GET':
		special_offers_list =  SpecialoffersUnderCategory.objects.values('id',
		                                                                 'special_offers_id',
		                                                                 'special_offers_parent_category_id',
		                                                                 'telecom_name',
		                                                                 'telecom_logo',
		                                                                 'special_offers_sub_parent_category_id',
		                                                                 'special_offers_combo_name',
		                                                                 'special_offers_type_name',
		                                                                 'city_id',
		                                                                 'city_id__city_name',
		                                                                 'province_id',
		                                                                 'province_id__province_name',
		                                                                 'special_offers_parent_category_id__special_offers_parent_category_name',
		                                                                 'special_offers_sub_parent_category_id__special_offers_sub_parent_category_name','status').filter(pk=id)
		
		provinces = Province.objects.values('id', 'province_name', 'country_id__id', 'country_id__country_name')
		city = City.objects.values('id', 'city_name', 'province_id__province_name', 'province_id__id')
		
		parent_category_list = SpecialoffersParentCategory.objects.values('id', 'special_offers_parent_category_name')
		sub_parent_category_list = SpecialoffersSubParentCategory.objects.values('id', 'special_offers_parent_category_id',
		                                                                         'special_offers_sub_parent_category_name')
		
		special_offers_category = SpecialOffers.objects.values('id')
		
		
		
		return render(request, 'admin/frontend/special_offers/services_category/category/edit.html',
		              {'parent_category_list': parent_category_list, 'special_offers_list': special_offers_list,'id':id,
		               'sub_parent_category_list': sub_parent_category_list, 'special_offers_category': special_offers_category,
		               'provinces':provinces,
		               'city':city
		               })
	
	elif request.method == 'POST':
		so_Offers = SpecialoffersUnderCategory.objects.values('telecom_logo').filter(pk=id)
		form = SpecialoffersUnderCategoryForm(request.POST,request.FILES)
		data = SpecialoffersUnderCategory.objects.get(pk=id)
		if len(request.FILES) != 0:
			if form.is_valid():
				data.special_offers_parent_category_id = form['special_offers_parent_category'].data
				data.special_offers_sub_parent_category_id = form['special_offers_sub_parent_category'].data
				data.status = form['status'].data
				data.special_offers_combo_name = form['special_offers_combo_name'].data
				data.special_offers_type_name = form['special_offers_type_name'].data
				data.telecom_name = form['telecom_name'].data
				data.telecom_logo = request.FILES['telecom_logo']
				data.save()
				messages.add_message(request, messages.SUCCESS, 'Special Offers Section Category Update successfully')
				return HttpResponseRedirect(reverse('special_offers_category_edit', kwargs={'id': id}))
			else:
				messages.add_message(request, messages.ERROR, form.errors)
				return HttpResponseRedirect(reverse('special_offers_category_edit', kwargs={'id': id}))
		else:
			data.special_offers_parent_category_id = form['special_offers_parent_category'].data
			data.special_offers_sub_parent_category_id = form['special_offers_sub_parent_category'].data
			data.status = form['status'].data
			data.special_offers_combo_name = form['special_offers_combo_name'].data
			data.special_offers_type_name = form['special_offers_type_name'].data
			data.telecom_name = form['telecom_name'].data
			data.telecom_logo = so_Offers[0]['telecom_logo']
			data.save()
			messages.add_message(request, messages.SUCCESS, 'Special Offers Section Category Update successfully')
			return HttpResponseRedirect(reverse('special_offers_category_edit', kwargs={'id': id}))


# Delete Special Offers Under Category

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def special_offers_category_delete(request,id):
	if request.method == 'GET':
		if SpecialoffersUnderCategory.objects.filter(pk=id).exists():
			SpecialoffersUnderCategory.objects.filter(pk=id).delete()
			messages.add_message(request, messages.SUCCESS, 'Special Offers Section Category Deleted Successfully')
			return HttpResponseRedirect(reverse('special_offers_category_list'))
		else:
			# messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('special_offers_category_list'))




@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def get_sub_special_offers_parent_list(request):
	if request.is_ajax():
		category_id = request.POST['category']
		manage_service_price = SpecialoffersSubParentCategory.objects.values('id', 'special_offers_parent_category_id',
		                                                                     'special_offers_sub_parent_category_name').filter(special_offers_parent_category_id=category_id)
		data = render_to_string('admin/frontend/special_offers/services_category/category/list.html',
		                        {'manage_service_price': manage_service_price})
		return HttpResponse(json.dumps({'data': data}), content_type="application/json")


def get_city(request):
	if request.is_ajax():
		id = request.POST['province']
		city = City.objects.values('id','city_name').filter(province_id__id=id)
		data = render_to_string('admin/frontend/special_offers/services_category/category/city_list.html',
		                        {'cities': city})
		return HttpResponse(json.dumps({'data': data}), content_type="application/json")










# Front End

@csrf_exempt
def get_set_of_special_offers(request):
	if request.is_ajax():
		id = request.POST['id']
		p_id = request.POST['parent_id']
		sp = SpecialoffersUnderCategory.objects.values('id',
		                                               'special_offers_parent_category_id',
		                                               'special_offers_parent_category_id__special_offers_parent_category_name',
		                                               'special_offers_parent_category_id__desc',
		                                               'special_offers_sub_parent_category_id',
		                                               'special_offers_sub_parent_category_id__special_offers_sub_parent_category_name',
		                                               'special_offers_sub_parent_category_id__desc',
		                                               'special_offers_combo_name',
		                                               'special_offers_type_name',
		                                               'province_id',
		                                               'province_id__province_name',
		                                               'city_id',
		                                               'city_id__city_name',
		                                               'telecom_name',
		                                               'telecom_logo',
		                                               'status',
		                                               ).filter(special_offers_sub_parent_category_id=id,special_offers_parent_category_id=p_id)#.distinct('special_offers_combo_name')
		
		print(len(sp))
		distinct_sp = SpecialoffersUnderCategory.objects.values('special_offers_combo_name').distinct('special_offers_combo_name')
		data = []
		print(distinct_sp)
		for combo_name in distinct_sp:
			combo_dict = {}
			distinct_types = SpecialoffersUnderCategory.objects.values('special_offers_type_name').filter(
				special_offers_sub_parent_category_id=id,
				special_offers_parent_category_id=p_id,
				special_offers_combo_name=combo_name['special_offers_combo_name']).distinct('special_offers_type_name')
			combo_dict['special_offers_combo_name'] = combo_name['special_offers_combo_name']
			combo_dict['data'] = []
			print(distinct_types)
			for offer_type in distinct_types:
				offer_dict = {}
				offer_dict['type_name'] = offer_type['special_offers_type_name']
				offer_dict['data'] = []
				obj = SpecialoffersUnderCategory.objects.values('id',
				                                                'special_offers_parent_category_id',
				                                                'special_offers_parent_category_id__special_offers_parent_category_name',
				                                                'special_offers_parent_category_id__desc',
				                                                'special_offers_sub_parent_category_id',
				                                                'special_offers_sub_parent_category_id__special_offers_sub_parent_category_name',
				                                                'special_offers_sub_parent_category_id__desc',
				                                                'special_offers_combo_name',
				                                                'special_offers_type_name',
				                                                'province_id',
				                                                'province_id__province_name',
				                                                'city_id',
				                                                'city_id__city_name',
				                                                'telecom_name',
				                                                'telecom_logo',
				                                                'status',).filter(
					special_offers_sub_parent_category_id=id,
					special_offers_parent_category_id=p_id,
					special_offers_combo_name=combo_name['special_offers_combo_name'],
					special_offers_type_name=offer_type['special_offers_type_name'])
				
				offer_dict['data'] = list(obj)
				combo_dict['data'].append(offer_dict)
			
			# combo_dict['data'] = list(set(combo_dict['data']))
			data.append(combo_dict)
		rendered = render_to_string('egciptv/special_offers/special_offers_dt_list.html',
		                            {'sp': sp, 'distinct_sp': distinct_sp, 'special_offer_data': data})
		# print('rendered')
		print(data)
		return HttpResponse(json.dumps({'data': rendered}), content_type="application/json")

def get_details_of_special_offers(request,type_name,combo_name,parent_id,sub_parent_id):
	if request.method=='GET':
		sp = SpecialoffersUnderCategory.objects.values('id',
		                                               'special_offers_parent_category_id',
		                                               'special_offers_parent_category_id__special_offers_parent_category_name',
		                                               'special_offers_parent_category_id__desc',
		                                               'special_offers_sub_parent_category_id',
		                                               'special_offers_sub_parent_category_id__special_offers_sub_parent_category_name',
		                                               'special_offers_sub_parent_category_id__desc',
		                                               'special_offers_combo_name',
		                                               'special_offers_type_name',
		                                               'province_id',
		                                               'province_id__province_name',
		                                               'city_id',
		                                               'city_id__city_name',
		                                               'telecom_name',
		                                               'telecom_logo',
		                                               'status',
		                                               'special_offers_id',
		                                               'special_offers_id__actual_price',
		                                               'special_offers_id__offers_price',
		                                               'special_offers_id__details',
		                                               ).filter(special_offers_parent_category_id=parent_id,special_offers_sub_parent_category_id=sub_parent_id,special_offers_combo_name=combo_name,special_offers_type_name=type_name)
		return render(request, 'egciptv/special_offers/special_offers_deatils.html',
		              {'sp': sp,'combo_name':combo_name,'type_name':type_name,'parent_id':parent_id,'sub_parent_id':sub_parent_id})


def get_data_according_to_type(request):
	if request.is_ajax():
		p_id = request.POST['p_id']
		sub_p_id=request.POST['sub_p_id']
		combo_name=request.POST['combo_name']
		type_name=request.POST['type_name']
		sp = SpecialoffersUnderCategory.objects.values('id',
		                                               'special_offers_parent_category_id',
		                                               'special_offers_parent_category_id__special_offers_parent_category_name',
		                                               'special_offers_parent_category_id__desc',
		                                               'special_offers_sub_parent_category_id',
		                                               'special_offers_sub_parent_category_id__special_offers_sub_parent_category_name',
		                                               'special_offers_sub_parent_category_id__desc',
		                                               'special_offers_combo_name',
		                                               'special_offers_type_name',
		                                               'province_id',
		                                               'province_id__province_name',
		                                               'city_id',
		                                               'city_id__city_name',
		                                               'telecom_name',
		                                               'telecom_logo',
		                                               'status',
		                                               'special_offers_id',
		                                               'special_offers_id__actual_price',
		                                               'special_offers_id__offers_price',
		                                               'special_offers_id__details',
		                                               ).filter(special_offers_parent_category_id=p_id,
		                                                        special_offers_sub_parent_category_id=sub_p_id,
		                                                        special_offers_combo_name=combo_name,
		                                                        special_offers_type_name=type_name)
		
		
		data = render_to_string('egciptv/special_offers/special_offers_type_dt_list.html',
		                        {'sp': sp})
		return HttpResponse(json.dumps({'data': data}), content_type="application/json")


def get_special_offers_plan_details(request,id):
	if request.method =='GET':
		sp = SpecialoffersUnderCategory.objects.values('id',
		                                               'special_offers_parent_category_id',
		                                               'special_offers_parent_category_id__special_offers_parent_category_name',
		                                               'special_offers_parent_category_id__desc',
		                                               'special_offers_sub_parent_category_id',
		                                               'special_offers_sub_parent_category_id__special_offers_sub_parent_category_name',
		                                               'special_offers_sub_parent_category_id__desc',
		                                               'special_offers_combo_name',
		                                               'special_offers_type_name',
		                                               'province_id',
		                                               'province_id__province_name',
		                                               'city_id',
		                                               'city_id__city_name',
		                                               'telecom_name',
		                                               'telecom_logo',
		                                               'status',
		                                               'special_offers_id',
		                                               'special_offers_id__actual_price',
		                                               'special_offers_id__offers_price',
		                                               'special_offers_id__details',
		                                               ).filter(pk=id)
		return render(request, 'egciptv/special_offers/special_o.html',{'sp': sp})

		
		
		
		
		