from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect,HttpResponse,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from crmadmin.models import ManageServicesPriceCategory
from sitefrontendbyadmin.forms import MenuCategoryForm,MenuSubParentCategoryForm,MenuParentCategoryForm,ServicefeaturesForm,SliderForm
from sitefrontendbyadmin.models import MenuParentCategory,MenuSubParentCategory,MenuCategory
from sitefrontendbyadmin.models import serviceandfeature,Slider,Network_status,FAQ,Followus,WebLogo, BackgroundImage
from django.contrib import messages
from django.urls import reverse
import requests
import json


def my_check(user):
	return user.is_superuser == True

#======================================================================= Parent Category ==========================================================================================================================


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def menu_parent_category_list(request):
		if request.method == 'GET':
			menu_list = MenuParentCategory.objects.values('id','service_parent_category_name','status')
			return render(request, 'admin/frontend/menu/parent/index.html',{'menu_list':menu_list})


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def menu_parent_category_add(request):
	if request.method == 'GET':
		category_list = MenuParentCategory.objects.values('id','service_parent_category_name','status')
		return render(request, 'admin/frontend/menu/parent/add.html',{'category_list':category_list})
	
	elif request.method == 'POST':
		form = MenuParentCategoryForm(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Menu Section Parent Category Added successfully')
			return HttpResponseRedirect(reverse('menu_parent_category_add'))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('menu_parent_category_add'))


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def menu_parent_category_edit(request,id):
	if request.method == 'GET':
		for_edited_menu = MenuParentCategory.objects.values('id','service_parent_category_name','status').filter(pk=id)
		
		return render(request, 'admin/frontend/menu/parent/edit.html', {'for_edited_menu': for_edited_menu})
	
	elif request.method == 'POST':
		data = MenuParentCategory.objects.get(pk=id)
		form = MenuParentCategoryForm(request.POST)
		if form.is_valid():
			data.service_parent_category_name=form['service_parent_category_name'].data
			data.status=form['status'].data
			data.save()
			messages.add_message(request, messages.SUCCESS, 'Menu Section Parent Category Updated successfully')
			return HttpResponseRedirect(reverse('menu_parent_category_edit',kwargs={'id':id}))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('menu_parent_category_edit',kwargs={'id':id}))

#======================================================================= Parent Sub Category ==========================================================================================================================

@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def menu_parent_sub_category_list(request):
	if request.method == 'GET':
		menu_list = MenuSubParentCategory.objects.values('id', 'service_sub_parent_category_name','service_parent_category_id__service_parent_category_name','status')
		return render(request, 'admin/frontend/menu/subparent/index.html', {'menu_list': menu_list})


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def menu_parent_sub_category_add(request):
	if request.method == 'GET':
		category_list = MenuSubParentCategory.objects.values('id', 'service_sub_parent_category_name','status')
		parent_category_list = MenuParentCategory.objects.values('id', 'service_parent_category_name','status').filter(status='active')
		return render(request, 'admin/frontend/menu/subparent/add.html', {'category_list': category_list,'parent_category_list':parent_category_list})
	
	elif request.method == 'POST':
		form = MenuSubParentCategoryForm(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Menu Section Sub Parent Category Added successfully')
			return HttpResponseRedirect(reverse('menu_parent_sub_category_add'))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('menu_parent_sub_category_add'))


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def menu_sub_parent_category_edit(request, id):
	if request.method == 'GET':
		
		parent_menu = MenuSubParentCategory.objects.values('id',
		                                                   'service_parent_category_id',
		                                                   'service_sub_parent_category_name','status').filter(pk=id)
		
		category_list = MenuParentCategory.objects.values('id',
		                                                  'service_parent_category_name','status').filter(pk=parent_menu[0]['service_parent_category_id'],status='active')
		
		for_edited_menu = MenuSubParentCategory.objects.values('id',
		                                                       'service_parent_category_id',
		                                                       'service_sub_parent_category_name','status').filter(pk=id)
		
		return render(request, 'admin/frontend/menu/subparent/edit.html', {'for_edited_menu': for_edited_menu,'category_list':category_list})
	
	elif request.method == 'POST':
		data = MenuSubParentCategory.objects.get(pk=id)
		form = MenuSubParentCategoryForm(request.POST)
		if form.is_valid():
			data.service_sub_parent_category_name = form['service_sub_parent_category_name'].data
			data.status = form['status'].data
			data.save()
			messages.add_message(request, messages.SUCCESS, 'Menu Section Sub Parent Category Updated successfully')
			return HttpResponseRedirect(reverse('menu_parent_sub_category_edit', kwargs={'id': id}))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('menu_parent_sub_category_edit', kwargs={'id': id}))
		
		
#======================================================================= Category ==========================================================================================================================
@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def menu_category_list(request):
	if request.method == 'GET':
		menu_list = MenuCategory.objects.values('id',
		                                        'service_parent_category_id',
		                                        'service_category_id__service_category_name',
		                                        'service_parent_category_id__service_parent_category_name',
		                                        'service_sub_parent_category_name_id',
		                                        'status',
		                                        'service_sub_parent_category_name_id__service_sub_parent_category_name')
		return render(request, 'admin/frontend/menu/category/index.html', {'menu_list': menu_list})


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def menu_category_add(request):
	if request.method == 'GET':
		parent_category_list = MenuParentCategory.objects.values('id', 'service_parent_category_name').filter(status='active')
		menu_list = ManageServicesPriceCategory.objects.values('id', 'service_category_name').filter(status='active')
		return render(request, 'admin/frontend/menu/category/add.html',
		              {'parent_category_list': parent_category_list,'menu_list':menu_list
		               })
	
	elif request.method == 'POST':
		form = MenuCategoryForm(request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Menu Section Category Added successfully')
			return HttpResponseRedirect(reverse('menu_category_add'))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('menu_category_add'))
		
		
@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def menu_category_edit(request,id):
	if request.method == 'GET':
		menu_list = MenuCategory.objects.values('id',
		                                        'service_parent_category_id',
		                                        'service_category_id__service_category_name',
		                                        'service_parent_category_id__service_parent_category_name',
		                                        'service_category_id',
		                                        'service_sub_parent_category_name_id',
		                                        'status',
		                                        'service_sub_parent_category_name_id__service_sub_parent_category_name').filter(pk=id)
		parent_category_list = MenuParentCategory.objects.values('id', 'service_parent_category_name').filter(status='active')
		sub_parent_category_list = MenuSubParentCategory.objects.values('id', 'service_parent_category_id','service_sub_parent_category_name').filter(status='active')
		menu_category = ManageServicesPriceCategory.objects.values('id', 'service_category_name').filter(status='active')
		return render(request, 'admin/frontend/menu/category/edit.html',
		              {'parent_category_list': parent_category_list, 'menu_list': menu_list,'sub_parent_category_list':sub_parent_category_list,'menu_category':menu_category
		               })
	
	elif request.method == 'POST':
		form = MenuCategoryForm(request.POST)
		data = MenuCategory.objects.get(pk=id)
		if form.is_valid():
			data.status=form['status'].data
			data.service_parent_category_id = request.POST['service_parent_category']
			data.service_category_id = request.POST['service_category']
			data.service_sub_parent_category_name_id = request.POST['service_sub_parent_category_name']
			data.save()
			messages.add_message(request, messages.SUCCESS, 'Menu Section Category Update successfully')
			return HttpResponseRedirect(reverse('menu_category_edit',kwargs={'id':id}))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('menu_category_edit',kwargs={'id':id}))



@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def get_sub_parent_list(request):
    if request.is_ajax():
        category_id = request.POST['category']
        manage_service_price = MenuSubParentCategory.objects.values('id', 'service_parent_category_id','service_sub_parent_category_name').filter(service_parent_category_id=category_id)
        data = render_to_string('admin/frontend/menu/category/list.html', {'manage_service_price': manage_service_price})
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")


# ======================================================================= Service Features ==========================================================================================================================
@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def service_feature_list(request):
	if request.method == 'GET':
		menu_list = serviceandfeature.objects.values('id',
		                                        'service_parent_category_id',
		                                        'service_category_id__service_category_name',
		                                        'service_parent_category_id__service_parent_category_name',
		                                        'service_sub_parent_category_name_id',
		                                        'details',
		                                        'service_feature_logo',
		                                        'service_sub_parent_category_name_id__service_sub_parent_category_name','status')
		return render(request, 'admin/frontend/serviceandfeatures/index.html', {'menu_list': menu_list})


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def service_feature_add(request):
	if request.method == 'GET':
		parent_category_list = MenuParentCategory.objects.values('id', 'service_parent_category_name').filter(status='active')
		menu_list = ManageServicesPriceCategory.objects.values('id', 'service_category_name').filter(status='active')
		return render(request, 'admin/frontend/serviceandfeatures/add.html',
		              {'parent_category_list': parent_category_list, 'menu_list': menu_list
		               })
	
	elif request.method == 'POST':
		form = ServicefeaturesForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Service Features Added successfully')
			return HttpResponseRedirect(reverse('service_feature_add'))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('service_feature_add'))


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def service_feature_edit(request, id):
	if request.method == 'GET':
		menu_list = serviceandfeature.objects.values('id',
		                                        'service_parent_category_id',
		                                        'service_category_id__service_category_name',
		                                        'service_parent_category_id__service_parent_category_name',
		                                        'service_category_id',
		                                        'service_sub_parent_category_name_id',
		                                        'details',
		                                        'service_feature_logo',
		                                        'service_sub_parent_category_name_id__service_sub_parent_category_name','status').filter(
			pk=id)
		parent_category_list = MenuParentCategory.objects.values('id', 'service_parent_category_name').filter(status='active')
		sub_parent_category_list = MenuSubParentCategory.objects.values('id', 'service_parent_category_id',
		                                                                'service_sub_parent_category_name').filter(status='active')
		menu_category = ManageServicesPriceCategory.objects.values('id', 'service_category_name').filter(
			status='active')
		return render(request, 'admin/frontend/serviceandfeatures/edit.html',
		              {'parent_category_list': parent_category_list, 'menu_list': menu_list,
		               'sub_parent_category_list': sub_parent_category_list, 'menu_category': menu_category
		               })
	
	elif request.method == 'POST':
		serviceF = serviceandfeature.objects.values('service_feature_logo').filter(pk=id)
		form = ServicefeaturesForm(request.POST,request.FILES)
		try:
			data = serviceandfeature.objects.get(pk=id)
			if len(request.FILES) != 0:
				if form.is_valid():
					data.service_parent_category_id = request.POST['service_parent_category']
					data.service_sub_parent_category_name_id = request.POST['service_sub_parent_category_name']
					data.service_category_id = request.POST['service_category']
					data.details = form['details'].data
					data.status = form['status'].data
					data.service_feature_logo = request.FILES['service_feature_logo']
					data.save()
					messages.add_message(request, messages.SUCCESS, 'Service Features Updated successfully')
					return HttpResponseRedirect(reverse('service_feature_edit', kwargs={'id': id}))
				else:
					messages.add_message(request, messages.ERROR, form.errors)
					return HttpResponseRedirect(reverse('service_feature_edit', kwargs={'id': id}))
			
			
			else:
				data.service_parent_category_id = request.POST['service_parent_category']
				data.service_sub_parent_category_name_id = request.POST['service_sub_parent_category_name']
				data.service_category_id = request.POST['service_category']
				data.details = request.POST['details']
				data.status = request.POST['status']
				data.service_feature_logo = serviceF[0]['service_feature_logo']
				data.save()
				messages.add_message(request, messages.SUCCESS, 'Service Features Updated successfully')
				return HttpResponseRedirect(reverse('service_feature_edit', kwargs={'id': id}))
		except serviceandfeature.DoesNotExist:
			data = None
			messages.add_message(request, messages.ERROR, 'Error')
			return HttpResponseRedirect(reverse('service_feature_edit', kwargs={'id': id}))
		

# ======================================================================= Slider ==========================================================================================================================


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def slider_index(request):
	if request.method == 'GET':
		slider = Slider.objects.values('id', 'slider_name','details','image','url','status')
		return render(request, 'admin/frontend/slider/index.html',{'slider':slider})
		
		
@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def slider_add(request):
	if request.method == 'GET':
		return render(request, 'admin/frontend/slider/add.html')
	elif request.method == 'POST':
		form = SliderForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Slider Added successfully')
			return HttpResponseRedirect(reverse('slider_add'))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('slider_add'))
		
@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def slider_edit(request,id):
	if request.method == 'GET':
		slider = Slider.objects.values('id', 'slider_name', 'details', 'image', 'url', 'status').filter(pk=id)
		return render(request, 'admin/frontend/slider/edit.html',{'slider':slider})
	elif request.method == 'POST':
		slider = Slider.objects.values('id', 'slider_name', 'details', 'image', 'url', 'status').filter(pk=id)
		data = Slider.objects.get(pk=id)
		form = SliderForm(request.POST,request.FILES)
		if len(request.FILES) != 0:
			if form.is_valid():
				data.slider_name=form['slider_name'].data
				data.details=form['details'].data
				data.image=request.FILES['image']
				data.url=form['url'].data
				data.status=form['status'].data
				data.save()
				messages.add_message(request, messages.SUCCESS, 'Slider Updated successfully')
				return HttpResponseRedirect(reverse('slider_edit',kwargs={'id':id}))
			else:
				messages.add_message(request, messages.ERROR, form.errors)
				return HttpResponseRedirect(reverse('slider_edit',kwargs={'id':id}))
		else:
			data.slider_name = request.POST['slider_name']
			data.details = request.POST['details']
			data.image = slider[0]['image']
			data.url = request.POST['url']
			data.status = request.POST['status']
			data.save()
			messages.add_message(request, messages.SUCCESS, 'Slider Updated successfully')
			return HttpResponseRedirect(reverse('slider_edit', kwargs={'id': id}))
		


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def slider_delete(request,id):
	if request.method == 'GET':
		if Slider.objects.filter(pk=id).exists():
			Slider.objects.delete().filter(pk=id)
			messages.add_message(request, messages.SUCCESS, 'Slider Deleted successfully')
			return HttpResponseRedirect(reverse('slider_index'))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('slider_index'))


# ======================================================================= Network Status ==========================================================================================================================
@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def network_status_index(request):
	if request.method == 'GET':
		network_status = Network_status.objects.values('id', 'questions', 'answers', 'docs', 'link')
		return render(request, 'admin/frontend/network_status/index.html', {'network_status': network_status})


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def network_status_add(request):
	if request.method == 'GET':
		return render(request, 'admin/frontend/network_status/add.html')
	elif request.method == 'POST':
		try:
			if "docs" in request.FILES.keys() and request.POST['link'] == '':
				Network_status.objects.create(questions=request.POST['questions'],
				                              answers=request.POST['answers'],
				                              docs=request.FILES['docs'],
				                              )
				
				messages.add_message(request, messages.SUCCESS, 'Network Status Added successfully')
				return HttpResponseRedirect(reverse('network_status_add'))
			
			elif "docs" in request.FILES.keys() and "link" in request.POST.keys():
				
				Network_status.objects.create(questions=request.POST['questions'],
				                              answers=request.POST['answers'],
				                              docs=request.FILES['docs'],
				                              link=request.POST['link'],
				                              )
				
				messages.add_message(request, messages.SUCCESS, 'Network Status Added successfully')
				return HttpResponseRedirect(reverse('network_status_add'))
				
			else:
				Network_status.objects.create(questions=request.POST['questions'],
				                              answers=request.POST['answers'],
				                              link=request.POST['link'],
				                              docs='None'
				                              )
				
				messages.add_message(request, messages.SUCCESS, 'Network Status Added successfully')
				return HttpResponseRedirect(reverse('network_status_add'))
				
				
		except Exception as e:
			print(e)
			messages.add_message(request, messages.ERROR, e)
			return HttpResponseRedirect(reverse('network_status_add'))


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def network_status_edit(request, id):
	if request.method == 'GET':
		network_status = Network_status.objects.values('id', 'questions', 'answers', 'docs', 'link').filter(pk=id)
		return render(request, 'admin/frontend/network_status/edit.html', {'network_status': network_status})
	elif request.method == 'POST':
		data = Network_status.objects.get(pk=id)
		try:
			if "docs" in request.FILES.keys() and request.POST['link'] == '':
				data.questions = request.POST['questions']
				data.answers = request.POST['answers']
				data.docs = request.FILES['docs']
				data.save()
				messages.add_message(request, messages.SUCCESS, 'Network Status Updated successfully')
				return HttpResponseRedirect(reverse('network_status_edit', kwargs={'id': id}))
				
			elif "docs" in request.FILES.keys() and "link" in request.POST.keys():
				data.questions = request.POST['questions']
				data.answers = request.POST['answers']
				data.docs = request.FILES['docs']
				data.link = request.POST['link']
				data.save()
				messages.add_message(request, messages.SUCCESS, 'Network Status Updated successfully')
				return HttpResponseRedirect(reverse('network_status_edit', kwargs={'id': id}))
			
			else:
				data.questions = request.POST['questions']
				data.answers = request.POST['answers']
				data.link = request.POST['link']
				data.save()
				messages.add_message(request, messages.SUCCESS, 'Network Status Updated successfully')
				return HttpResponseRedirect(reverse('network_status_edit', kwargs={'id': id}))
	
		except Exception as e:
			messages.add_message(request, messages.ERROR, e)
			return HttpResponseRedirect(reverse('network_status_edit', kwargs={'id': id}))


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def network_status_delete(request, id):
	if request.method == 'GET':
		if Network_status.objects.filter(pk=id).exists():
			Network_status.objects.delete().filter(pk=id)
			messages.add_message(request, messages.SUCCESS, 'Network Status Deleted successfully')
			return HttpResponseRedirect(reverse('network_status_index'))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('network_status_index'))


# ======================================================================= FAQs ==========================================================================================================================
@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def faq_index(request):
	if request.method == 'GET':
		faq = FAQ.objects.values('id', 'questions', 'answers', 'docs', 'link')
		return render(request, 'admin/frontend/faq/index.html', {'faq': faq})


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def faq_add(request):
	if request.method == 'GET':
		return render(request, 'admin/frontend/faq/add.html')
	elif request.method == 'POST':
		try:
			if "docs" in request.FILES.keys() and request.POST['link'] == '':
				FAQ.objects.create(questions=request.POST['questions'],
				                              answers=request.POST['answers'],
				                              docs=request.FILES['docs'],
				                              )
				
				messages.add_message(request, messages.SUCCESS, 'Network Status Added successfully')
				return HttpResponseRedirect(reverse('faq_add'))
			
			elif "docs" in request.FILES.keys() and "link" in request.POST.keys():
				
				FAQ.objects.create(questions=request.POST['questions'],
				                              answers=request.POST['answers'],
				                              docs=request.FILES['docs'],
				                              link=request.POST['link'],
				                              )
				
				messages.add_message(request, messages.SUCCESS, 'Network Status Added successfully')
				return HttpResponseRedirect(reverse('faq_add'))
			
			else:
				FAQ.objects.create(questions=request.POST['questions'],
				                              answers=request.POST['answers'],
				                              link=request.POST['link'],
				                              docs='None'
				                              )
				
				messages.add_message(request, messages.SUCCESS, 'Network Status Added successfully')
				return HttpResponseRedirect(reverse('faq_add'))
		except Exception as e:
			messages.add_message(request, messages.ERROR, e)
			return HttpResponseRedirect(reverse('faq_add'))


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def faq_edit(request, id):
	if request.method == 'GET':
		faq = FAQ.objects.values('id', 'questions', 'answers', 'docs', 'link').filter(pk=id)
		return render(request, 'admin/frontend/faq/edit.html', {'faq': faq})
	elif request.method == 'POST':
		data = FAQ.objects.get(pk=id)
		try:
			if "docs" in request.FILES.keys() and request.POST['link'] == '':
				data.questions = request.POST['questions']
				data.answers = request.POST['answers']
				data.docs = request.FILES['docs']
				data.save()
				messages.add_message(request, messages.SUCCESS, 'FAQ Updated successfully')
				return HttpResponseRedirect(reverse('faq_edit', kwargs={'id': id}))
			
			elif "docs" in request.FILES.keys() and "link" in request.POST.keys():
				data.questions = request.POST['questions']
				data.answers = request.POST['answers']
				data.docs = request.FILES['docs']
				data.link = request.POST['link']
				data.save()
				messages.add_message(request, messages.SUCCESS, 'FAQs Updated successfully')
				return HttpResponseRedirect(reverse('faq_edit', kwargs={'id': id}))
			
			else:
				data.questions = request.POST['questions']
				data.answers = request.POST['answers']
				data.link = request.POST['link']
				data.save()
				messages.add_message(request, messages.SUCCESS, 'FAQ Updated successfully')
				return HttpResponseRedirect(reverse('faq_edit', kwargs={'id': id}))
		
		except Exception as e:
			messages.add_message(request, messages.ERROR, e)
			return HttpResponseRedirect(reverse('faq_edit', kwargs={'id': id}))


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def faq_delete(request, id):
	if request.method == 'GET':
		if FAQ.objects.filter(pk=id).exists():
			FAQ.objects.delete().filter(pk=id)
			messages.add_message(request, messages.SUCCESS, 'FAQ Deleted successfully')
			return HttpResponseRedirect(reverse('faq_index'))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('faq_index'))


# ======================================================================= Follow Us ==========================================================================================================================
@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def follow_us_index(request):
	if request.method == 'GET':
		follow_us = Followus.objects.values('id', 'url', 'fa_fa_icon', 'status')
		return render(request, 'admin/frontend/follow_us/index.html', {'follow_us': follow_us})


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def follow_us_add(request):
	if request.method == 'GET':
		return render(request, 'admin/frontend/follow_us/add.html')
	elif request.method == 'POST':
		try:
			Followus.objects.create(url=request.POST['url'],
			                        status=request.POST['status']
				                   )
				
			messages.add_message(request, messages.SUCCESS, 'New link added successfully')
			return HttpResponseRedirect(reverse('follow_us_add'))
			
		except Exception as e:
			messages.add_message(request, messages.ERROR, e)
			return HttpResponseRedirect(reverse('follow_us_add'))


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def follow_us_edit(request, id):
	if request.method == 'GET':
		follow_us = Followus.objects.values('id', 'url', 'fa_fa_icon', 'status').filter(pk=id)
		return render(request, 'admin/frontend/follow_us/edit.html', {'follow_us': follow_us})
	elif request.method == 'POST':
		data = Followus.objects.get(pk=id)
		try:
			data.url = request.POST['url']
			data.status = request.POST['status']
			data.save()
			messages.add_message(request, messages.SUCCESS, 'Old link Updated successfully')
			return HttpResponseRedirect(reverse('follow_us_edit', kwargs={'id': id}))
		
		except Exception as e:
			messages.add_message(request, messages.ERROR, e)
			return HttpResponseRedirect(reverse('follow_us_edit', kwargs={'id': id}))


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def follow_us_delete(request, id):
	if request.method == 'GET':
		if Followus.objects.filter(pk=id).exists():
			Followus.objects.filter(pk=id).delete()
			messages.add_message(request, messages.SUCCESS, 'Link Deleted successfully')
			return HttpResponseRedirect(reverse('follow_us_index'))
		else:
			messages.add_message(request, messages.ERROR, form.errors)
			return HttpResponseRedirect(reverse('follow_us_index'))


#======================================== Upload Logo Area ==============================================


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def logo_index(request):
	if request.method == 'GET':
		logo = WebLogo.objects.values('id','image')
		return render(request, 'admin/frontend/upload_logo/index.html',{'logo':logo})
	
	
@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def upload_logo_area(request):
	
	if request.method == 'GET':
	
		return render(request, 'admin/frontend/upload_logo/add.html')
	
	elif request.method == 'POST':
		
		WebLogo.objects.create(image=request.FILES['image'])
		messages.add_message(request, messages.SUCCESS, 'Uploaded successfully')
		return HttpResponseRedirect(reverse('upload_logo_area'))


@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def edit_logo_area(request,id):
	if request.method == 'GET':
		logo = WebLogo.objects.values('id','image')
		return render(request, 'admin/frontend/upload_logo/edit.html',{'logo':logo})
	
	elif request.method == 'POST':
		
		if WebLogo.objects.filter(pk=id).exists():
			_logo = WebLogo.objects.get(pk=id)
			_logo.image = request.FILES['image']
			_logo.save()
			
			messages.add_message(request, messages.SUCCESS, 'Edited successfully')
			return HttpResponseRedirect(reverse('edit_logo_area',kwargs={'id':id}))
		
		else:
			messages.add_message(request, messages.ERROR, 'Error Occuere')
			return HttpResponseRedirect(reverse('edit_logo_area',kwargs={'id':id}))



@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def background_list(request):
	if request.method == 'GET':
		queryset = BackgroundImage.objects.all()
		return render(request, 'admin/frontend/bg_image/index.html', {'queryset':queryset})



@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def background_add(request):
	
	if request.method == 'GET':
	
		return render(request, 'admin/frontend/bg_image/add.html')
	
	elif request.method == 'POST':
		
		BackgroundImage.objects.create(image=request.FILES['image'])
		messages.add_message(request, messages.SUCCESS, 'Uploaded successfully')
		return HttpResponseRedirect(reverse('bg_image_add'))



@login_required(login_url="/admin")
@user_passes_test(my_check, login_url='/admin')
def background_edit(request,id):
	if request.method == 'GET':
		bg_image = BackgroundImage.objects.get(id=id)
		return render(request, 'admin/frontend/bg_image/edit.html', {'bg_image':bg_image})
	
	elif request.method == 'POST':
		
		if BackgroundImage.objects.filter(pk=id).exists():
			bg_image = BackgroundImage.objects.get(pk=id)
			bg_image.image = request.FILES['image']
			bg_image.save()
			
			messages.add_message(request, messages.SUCCESS, 'Edited successfully')
			return HttpResponseRedirect(reverse('bg_image_edit',kwargs={'id':id}))
		
		else:
			messages.add_message(request, messages.ERROR, 'Something went wrong. - Pk {} does not exist.'.format(id))
			return HttpResponseRedirect(reverse('bg_image_edit',kwargs={'id':id}))