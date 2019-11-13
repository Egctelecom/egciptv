import datetime
import json
from crmadmin.forms import UserImageform
from crmadmin.models import UserImage
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login

# Create your views here.
from django.template.loader import render_to_string
from django.urls import reverse

from crmadmin.templatetags.admin_functions import random_number
from django.contrib.auth.decorators import user_passes_test

def admin_login(request):
    if request.method == 'GET':
        if request.user.is_authenticated():
            return HttpResponseRedirect('/admin/dashboard/')
        else:
            return render(request, 'admin/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password, is_superuser='True')
        if user is not None:
            if user.is_active:
                if user.is_superuser:
                  login(request,user)
                  current_user_id = request.user.id
                  if User.objects.filter(id=current_user_id).exists():
                      email = User.objects.values('email', 'username').filter(id=current_user_id)
                      image = UserImage.objects.values('avatardata').filter(user_id=current_user_id)
                      request.session['adminemail'] = email[0]['email']
                      request.session['user_id'] = request.user.id
                      request.session['username'] = email[0]['username']
                      # request.session['avatar'] = image[0]['avatardata']
                      currentdate = datetime.date.today()
                      request.session['currentdate'] = str(currentdate)

                  return HttpResponseRedirect('/admin/dashboard/')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Credentials')
            return HttpResponseRedirect(reverse('admin_login'))

def my_check(user):
    return user.is_superuser == True


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def admin_dashboard(request):
    current_user_id = request.user.id
    if User.objects.filter(id=current_user_id).exists():
        email = User.objects.values('email','username').filter(id=current_user_id)
        image = UserImage.objects.values('avatardata').filter(user_id=current_user_id)
        request.session['adminemail']= email[0]['email']
        request.session['user_id']= request.user.id
        request.session['username']= email[0]['username']
        # request.session['avatar']= image[0]['avatardata']
        currentdate = datetime.date.today()
        request.session['currentdate']=str(currentdate)

        return render(request, 'admin/dashboard.html', {'useremail':email, 'username':email[0]['username'], 'currentdate':currentdate})

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def admin_signout(request):
    logout(request)
    for sesskey in request.session.keys():
        del request.session[sesskey]
    return redirect("/admin")


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def user_info(request):
    current_user_id = request.user.id
    us = User.objects.values('username','email').filter(id=current_user_id)
    return render(request, 'admin/user_info/index.html',{'us':us})

#===================================================  Save Profile =======================================================================#

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def saveprofile(request):
    if request.is_ajax():
        email = request.POST['email']
        current_user_id = request.user.id
        if User.objects.filter(id=current_user_id).exists():
            USER = User.objects.get(id=current_user_id)
            USER.email = email
            USER.save()
            msg = 'Profile Updated'
            return JsonResponse(msg, safe=False)

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def save_avatar(request):
    current_user_id = request.user.id
    if User.objects.filter(id=current_user_id).exists():
     form = UserImageform(request.POST,request.FILES)
     if form.is_valid():
         form.save()
         request.session['message']='success'
         image = UserImage.objects.values('avatardata').filter(user_id=current_user_id)
         request.session['avatar'] = image[0]['avatardata']
         return HttpResponseRedirect(reverse('user_info'))
     else:
         request.session['message']='error'
         return HttpResponseRedirect(reverse('user_info'))
#===================================================  Forget password  ===================================================================#
def send_mail_for_forget_password(request):
    if request.is_ajax():
        email = request.POST['email']
        USER = User.objects.values('id').filter(email=email)
        current_user_id = USER[0]['id']
        request.session['user']=current_user_id
        if User.objects.filter(id=current_user_id,email=email).exists():
            subject = 'Request OTP from Trading CRM'
            massege = render_to_string('admin/mail/forgetpasswordemail')
            html_msg = render_to_string('admin/mail/forgetpasswordemail')
            randDATA = random_number()
            request.session['random']=randDATA
            print(randDATA)
            send_mail(subject, massege, 'test@25airport.com', [email], fail_silently=False,
                      html_message=html_msg)
            msg = 'A link send to your provided email address'
            data = render_to_string('admin/mail/otp.html', {"data":randDATA})
            return HttpResponse(json.dumps({"data": data,'msg':msg}), content_type="application/json")

def checkotp(request):
    if request.is_ajax():
        otp = request.POST['otp']
        saveotp = request.session['random']
        print(saveotp)
        if saveotp == otp:
            msg = 'Valid OTP'
            data = render_to_string('admin/mail/newoldpassword.html')
            return HttpResponse(json.dumps({"data": data,'msg': msg}), content_type="application/json")
        else:
            msg = 'Enter valid otp'
            data = render_to_string('admin/mail/newoldpassword.html')
            return HttpResponse(json.dumps({"data": data, 'msg': msg}), content_type="application/json")


def paswordchange(request):
    if request.is_ajax():
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        current_user_id = request.session['user']
        if new_password == confirm_password:
            uSER = User.objects.get(pk=current_user_id)
            uSER.set_password(new_password)
            uSER.save()
            msg = 'Your Password Be changed'
            return JsonResponse(msg,safe=False)

        else:
            msg = 'New password and confirm password should be matched'
            return JsonResponse(msg, safe=False)


