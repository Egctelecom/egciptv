from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.auth.decorators import user_passes_test
from agentpanel.models import Agent

def my_check(user):
    if Agent.objects.filter(user_id=user.id).exists():
        if user.is_superuser == False:
            data = True
            return data


@login_required(login_url="/agent")
@user_passes_test(my_check,login_url='/agent')
def add_pending_invoice_details(request,id):
    pass