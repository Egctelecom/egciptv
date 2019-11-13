from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from crmadmin.models import UserProfile

from django.contrib.auth.decorators import user_passes_test

def my_check(user):
    return user.is_superuser == True

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def settings_logins_add(request):
    if request.method == 'GET':
        return render(request, 'admin/settings/logins/add.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        login_type = request.POST['login_type']
        commissions_in_USD = request.POST['commissions_in_USD']
        commissions_in_percent = request.POST['commissions_in_percent']
        role = request.POST['role']
        extension = request.POST['extension']
        if commissions_in_USD == '' or commissions_in_percent== '' or extension == '' :
            commissions_in_USD = 0.0
            commissions_in_percent = 0.0
            extension= 0.0
        else:
            commissions_in_USD = request.POST['commissions_in_USD']
            commissions_in_percent = request.POST['commissions_in_percent']
            extension = request.POST['extension']
        try:
            userdata = User.objects.create(username=username,email=email)
            userCast = User.objects.get(pk=userdata.pk)
            userCast.set_password(password)
            userCast.save()
            try:
                UserProfile.objects.create(user_id=userdata.pk,login_type=login_type,commissions_in_USD=commissions_in_USD,commissions_in_percent=commissions_in_percent,role=role,extentions=extension)
                messages.add_message(request, messages.SUCCESS, 'Login User added successfully')
                return HttpResponseRedirect(reverse('settings_logins_add'))

            except UserProfile.DoesNotExist:

                messages.add_message(request, messages.ERROR, 'User created but profile not updated')
                return HttpResponseRedirect(reverse('settings_logins_add'))

        except User.DoesNotExist:

            messages.add_message(request, messages.ERROR, 'User not created')
            return HttpResponseRedirect(reverse('settings_logins_add'))

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def settings_logins_edit(request,pk):
    if request.method == 'GET':
        userdetails = UserProfile.objects.values('user_id', 'user_id__username','user_id__email','login_type', 'role',
                                                 'user_id__is_active', 'user_id__last_login').filter(user_id=pk)

        return render(request, 'admin/settings/logins/edit.html',{'pk':pk,'userdetails':userdetails})

    elif request.method == 'POST':
        password = request.POST['password']
        email = request.POST['email']
        login_type = request.POST['login_type']
        commissions_in_USD = request.POST['commissions_in_USD']
        commissions_in_percent = request.POST['commissions_in_percent']
        role = request.POST['role']
        extension = request.POST['extension']
        is_active = request.POST['is_active']
        if commissions_in_USD == '' or commissions_in_percent== '' or extension == '' :
            commissions_in_USD = 0.0
            commissions_in_percent = 0.0
            extension= 0.0
        else:
            commissions_in_USD = request.POST['commissions_in_USD']
            commissions_in_percent = request.POST['commissions_in_percent']
            extension = request.POST['extension']
        try:
            if password == '' or is_active == True:
                 userCast = User.objects.get(pk=pk)
                 userCast.email = email
                 userCast.is_active = True
                 userCast.save()
            else:
                userCast = User.objects.get(pk=pk)
                userCast.email = email
                userCast.is_active = False
                userCast.set_password(password)
                userCast.save()

            try:
                userPro = UserProfile.objects.get(user_id=pk)
                userPro.login_type=login_type
                userPro.commissions_in_USD=commissions_in_USD
                userPro.commissions_in_percent=commissions_in_percent
                userPro.role=role
                userPro.extentions=extension
                userPro.save()

                messages.add_message(request, messages.SUCCESS, 'Login User Update successfully')
                return HttpResponseRedirect(reverse('settings_logins_edit', kwargs={'pk': pk}))

            except UserProfile.DoesNotExist:

                messages.add_message(request, messages.ERROR, 'User updated but profile not updated')
                return HttpResponseRedirect(reverse('settings_logins_edit', kwargs={'pk': pk}))

        except User.DoesNotExist:

            messages.add_message(request, messages.ERROR, 'User not created')
            return HttpResponseRedirect(reverse('settings_logins_edit', kwargs={'pk': pk}))


