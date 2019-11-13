from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test

def my_check(user):
    return user.is_superuser == True


@login_required(login_url="/admin")
@user_passes_test(my_check,login_url='/admin')
def add_pending_invoice_details(request,id):
    pass