from django.shortcuts import render
from adminsideserviceprovider.models import ServiceProvider, ServiceProviderPlan, CustomerWithService,CustomerServiceContract
from django.contrib.auth.decorators import user_passes_test
from egciptvhome.models import Otherdetails
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.urls import reverse

def my_check(user):
    return user.is_superuser == True


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def index_others_details(request):
	if request.method =='GET':
		details = Otherdetails.objects.values('id','key','value')
		return render(request, 'admin/frontend/others_section/index.html', {'details': details})
	
	
@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def add_others_details(request):
	if request.method =='GET':
		details = Otherdetails.objects.values('id','key','value')
		return render(request, 'admin/frontend/others_section/add.html', {'details': details})
	elif request.method =='POST':
		Otherdetails.objects.create(key=request.POST['key'],value=request.POST['editordata'])
		messages.add_message(request, messages.SUCCESS, 'Other details add successfully')
		return HttpResponseRedirect(reverse('add_others_details'))

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def edit_others_details(request,id):
	if request.method =='GET':
		details = Otherdetails.objects.values('id', 'key', 'value','address','country', 'city', 'province', 'zip', 'fax',
                                              'phone', 'email').filter(pk=id)
		return render(request, 'admin/frontend/others_section/edit.html', {'details': details})
	elif request.method == 'POST':
		if request.POST['key'] == 'About' or request.POST['key'] == 'Terms&Conditions' or request.POST['key'] == 'PrivacyPolicy' :
			details = Otherdetails.objects.get(pk=id)
			details.key = request.POST['key']
			details.value = request.POST['editordata']
			details.save()
		elif request.POST['key'] == 'Contact':
			details = Otherdetails.objects.get(pk=id)
			details.address = request.POST['address']
			details.city = request.POST['city']
			details.province = request.POST['province']
			details.country = request.POST['country']
			details.zip = request.POST['zip']
			details.fax = request.POST['fax']
			details.phone = request.POST['phone']
			details.email = request.POST['email']
			details.save()
		messages.add_message(request, messages.SUCCESS, 'Other details Updated successfully')
		return HttpResponseRedirect(reverse('edit_others_details',kwargs={'id':id}))
		