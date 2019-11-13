from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import render_to_string
from django.urls import reverse

from agentpanel.models import Agent
from django.contrib.auth.decorators import user_passes_test

def my_check(user):
    return user.is_superuser == True

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def agent_index(request):
    if request.method == 'GET':
        agent = Agent.objects.values('id','user_id','first_name','last_name','email_address','status')
        return render(request, 'admin/agent/index.html',{'agent':agent})

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def add_agent(request):
    if request.method == 'GET':
        return render(request, 'admin/agent/add.html')
    elif request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']

        passwrod = User.objects.make_random_password(length=14,
                                                     allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")

        user = User.objects.create(username=first_name,first_name=first_name,last_name=last_name,email=email)
        user.set_password(passwrod)
        user.save()
        agent = Agent.objects.create(user_id=user.id,first_name=first_name,last_name=last_name,phone=phone,email_address=email,status='Agent')
        agent.save()

        subject = 'Congratulations You are now agent of egciptv'
        massege = render_to_string('admin/agent/email.html',
                                   {'first_name': first_name, 'last_name':last_name,'passwrod':passwrod,'username':user.username})
        html_msg = render_to_string('admin/agent/email.html',
                                    {'first_name': first_name, 'last_name': last_name,'passwrod':passwrod,'username':user.username})
        send_mail(subject, massege, 'support@25airport.com', [email], fail_silently=False,
                  html_message=html_msg)

        messages.add_message(request, messages.SUCCESS, 'Agent Added Successfully')
        return HttpResponseRedirect(reverse('agent_add'))


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def edit_agent(request,pk):
    print(pk)
    if request.method == 'GET':
        agent = Agent.objects.values('id','user_id','first_name','last_name','phone','email_address','status').filter(pk=pk)
        return render(request, 'admin/agent/edit.html',{'agent':agent})
    elif request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']

        agentuser = Agent.objects.values('id','user_id','first_name','last_name','phone','email_address','status').filter(pk=pk)


        user = User.objects.get(pk=agentuser[0]['user_id'])
        user.username=first_name
        user.first_name=first_name
        user.last_name=last_name
        user.email=email
        user.save()

        agent = Agent.objects.get(pk=pk)
        agent.first_name=first_name
        agent.last_name=last_name
        agent.phone=phone
        agent.email_address=email
        agent.save()

        subject = 'egciptv | Your agent details updated'
        massege = render_to_string('admin/agent/update_email.html',
                                   {'first_name': first_name, 'last_name': last_name,
                                    'username': user.username})
        html_msg = render_to_string('admin/agent/update_email.html',
                                    {'first_name': first_name, 'last_name': last_name,
                                     'username': user.username})
        send_mail(subject, massege, 'support@25airport.com', [email], fail_silently=False,
                  html_message=html_msg)

        messages.add_message(request, messages.SUCCESS, 'Agent Added Successfully')
        return HttpResponseRedirect(reverse('agent_add'))

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def delete_agent(request,pk):
    if request.method == 'GET':
        if Agent.objects.filter(pk=pk).exists():
            agent = Agent.objects.values('id','user_id','first_name','last_name','email_address','status').filter(pk=pk)
            if User.objects.filter(pk=agent[0]['user_id']).exists():
                User.objects.filter(pk=agent[0]['user_id']).delete()
                Agent.objects.filter(pk=pk).delete()
                return HttpResponseRedirect(reverse('agent'))


