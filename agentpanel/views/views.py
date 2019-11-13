import datetime
import json

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
from agentpanel.models import Agent

from agentpanel.templatetags.admin_functions import random_number

from django.contrib.auth.decorators import user_passes_test

def my_check(user):
    if Agent.objects.filter(user_id=user.id).exists():
        if user.is_superuser == False:
            data = True
            return data


def agent_login(request):
    if request.method == 'GET':
        return render(request, 'agent/login.html')
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password, is_superuser='False')
        if user is not None:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect('/agent/dashboard/')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid Credentials')
            return HttpResponseRedirect(reverse('agent_login'))


@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def agent_dashboard(request):
    if request.user.is_superuser == False:
        current_user_id = request.user.id
        print(current_user_id)
        if User.objects.filter(id=current_user_id).exists():
            email = User.objects.values('email','username').filter(id=current_user_id)
            request.session['agentemail']= email[0]['email']
            request.session['username']= email[0]['username']
            currentdate = datetime.date.today()
            request.session['currentdate']=str(currentdate)

            return render(request, 'agent/dashboard.html', {'useremail':email, 'username':email[0]['username'], 'currentdate':currentdate})
    else:
        return HttpResponseRedirect(reverse('agent_login'))


@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def agent_signout(request):
    logout(request)
    return redirect("/agent")


#===================================================  Save Profile =======================================================================#
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
#===================================================  Forget password  ===================================================================#
def send_mail_for_forget_password(request):
    if request.is_ajax():
        email = request.POST['email']
        USER = User.objects.values('id').filter(email=email)
        current_user_id = USER[0]['id']
        request.session['user']=current_user_id
        if User.objects.filter(id=current_user_id,email=email).exists():
            subject = 'Request OTP from Trading CRM'
            massege = render_to_string('agent/mail/forgetpasswordemail')
            html_msg = render_to_string('agent/mail/forgetpasswordemail')
            randDATA = random_number()
            request.session['random']=randDATA
            print(randDATA)
            send_mail(subject, massege, 'test@25airport.com', [email], fail_silently=False,
                      html_message=html_msg)
            msg = 'A link send to your provided email address'
            data = render_to_string('agent/mail/otp.html', {"data":randDATA})
            return HttpResponse(json.dumps({"data": data,'msg':msg}), content_type="application/json")

def checkotp(request):
    if request.is_ajax():
        otp = request.POST['otp']
        saveotp = request.session['random']
        print(saveotp)
        if saveotp == otp:
            msg = 'Valid OTP'
            data = render_to_string('agent/mail/newoldpassword.html')
            return HttpResponse(json.dumps({"data": data,'msg': msg}), content_type="application/json")
        else:
            msg = 'Enter valid otp'
            data = render_to_string('agent/mail/newoldpassword.html')
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


