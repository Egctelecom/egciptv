import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Permission, User
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from agentpanel.models import Agent
from django.contrib.auth.decorators import user_passes_test

def my_check(user):
    return user.is_superuser == True

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def agent_index(request,pk):
    if request.method == 'GET':
        permission = Permission.objects.values('id','name','codename','content_type_id')
        agent = Agent.objects.values('id','first_name','last_name','email_address').filter(pk=pk)
        agentt = Agent.objects.values('user_id').filter(pk=pk)
        u = User.objects.get(pk=agentt[0]['user_id'])
        haveperm = u.get_all_permissions()
        # perm = u.has_perm('adminsidecustomer.add_city')
        return render(request, 'admin/agent/permission/index.html',{'agent':agent,'permission':permission,'user_id':agentt[0]['user_id'],'haveperm':haveperm})



@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def save_permission_to_agent(request):
    if request.is_ajax():
        agent_auto_id = request.POST["agent_id"]
        agent = Agent.objects.values('user_id').filter(pk=agent_auto_id)
        if User.objects.filter(pk=agent[0]['user_id']).exists():
             u = User.objects.get(pk=agent[0]['user_id'])
             json_permission = json.loads(request.POST['arrt'])
             for permission in json_permission:
              permission = Permission.objects.get(pk=permission)
              u.user_permissions.add(permission)
             response_data={}
             response_data['data']='success'
             return JsonResponse(response_data,safe=False)
        else:
            response_data = {}
            response_data['data'] = 'error'
            return JsonResponse(response_data, safe=False)


