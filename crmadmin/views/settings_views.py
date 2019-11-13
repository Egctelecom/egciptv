from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from crmadmin.models import ManageServicesPriceCategory,  UserProfile

from django.contrib.auth.decorators import user_passes_test

def my_check(user):
    return user.is_superuser == True

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def settings(request):
     if request.method == 'GET':
        servies_category = ManageServicesPriceCategory.objects.values('id', 'service_category_name', 'status')
        userdetails = UserProfile.objects.values('user_id','user_id__username', 'login_type', 'role', 'user_id__is_active', 'user_id__last_login')
        
        try:
            if request.session['tabName'] == 'manage_service_prices':
                 request.session['tabName']='manage_service_prices'
            else:
                request.session['tabName'] = 'logins'
        except Exception:
            request.session['tabName'] = 'logins'
        return render(request, 'admin/settings/index.html',{'servies_category':servies_category,'userdetails':userdetails})

