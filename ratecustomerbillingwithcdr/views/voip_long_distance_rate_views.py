from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import *
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import user_passes_test
from ratecustomerbillingwithcdr.models import VoipLongDistanceRate

def my_check(user):
    return user.is_superuser == True

class UploadFileForm(forms.Form):
    file = forms.FileField()


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def voip_distance_rate_view(request):
	if request.method == 'GET':
		data =VoipLongDistanceRate.objects.values('id','country','prefix','rate')
		return render(request, 'admin/areacode_with_rate/voip_distance_rate/index.html',{'data':data})
	


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def voip_distance_rate_excel_import(request):
    if request.method =='GET':
        return render(request, 'admin/areacode_with_rate/voip_distance_rate/import.html')
    elif request.method == "POST":
        form = UploadFileForm(request.POST,
                              request.FILES)

        if form.is_valid():
            request.FILES['file'].save_to_database(
                model=VoipLongDistanceRate,
                initializer=None,
                mapdict=['country',
                         'prefix',
                         'rate'])
            messages.add_message(request, messages.SUCCESS, 'Voip Long Distance Rate excel sheet imported successfully')
            return HttpResponseRedirect(reverse('voip_distance_rate_excel_import'))
        else:
            messages.add_message(request, messages.ERROR, form.errors)
            return HttpResponseRedirect(reverse('voip_distance_rate_excel_import'))
