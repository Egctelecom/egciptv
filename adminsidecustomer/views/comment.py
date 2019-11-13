from adminsidecustomer.models import CustomerComment
from adminsidecustomer.models import Customer
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import HttpResponse
import json
def my_check(user):
    return user.is_superuser == True

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def index(request,id):
    if request.method =='GET':
      data = CustomerComment.objects.filter(touser_id=id).values('id','user_id__first_name','touser_id','comment','created_at','user_id__is_superuser')
      return render(request, 'admin/users/comment/index.html', {  'comment': data,'customer_id':id })

@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def save_comment(request):
    if request.is_ajax():
        user = request.user.id
        touser =request.POST['customer_id']
        comment =request.POST['comment']
        da = CustomerComment.objects.create(user_id=user,touser_id=touser,comment=comment)
        da.save()
        ttsdata = CustomerComment.objects.filter(pk=da.id).values('id', 'user_id__first_name', 'touser_id', 'comment','created_at', 'user_id__is_superuser')
        data = render_to_string('admin/users/comment/list.html', {'comments': ttsdata})
        return HttpResponse(json.dumps({'data': data}), content_type="application/json")




