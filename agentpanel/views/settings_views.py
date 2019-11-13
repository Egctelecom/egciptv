from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from crmadmin.models import ManageServicesPriceCategory,  UserProfile
from django.contrib.auth.decorators import user_passes_test
from agentpanel.models import Agent

def my_check(user):
    if Agent.objects.filter(user_id=user.id).exists():
        if user.is_superuser == False:
            data = True
            return data

@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def settings(request):
     if request.method == 'GET':
        servies_category = ManageServicesPriceCategory.objects.values('id', 'service_category_name', 'status')
        userdetails = UserProfile.objects.values('user_id','user_id__username', 'login_type', 'role', 'user_id__is_active', 'user_id__last_login')
        return render(request, 'agent/settings/index.html',{'servies_category':servies_category,'userdetails':userdetails})

