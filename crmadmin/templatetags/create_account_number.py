from django import template
import string
import datetime
from django.contrib.auth.models import User

register = template.Library()


@register.simple_tag
def account_number():
    now = datetime.datetime.now().date().strftime("%Y%m%d")
    data = User.objects.values('id','first_name','last_name','email','date_joined')
    i=now+'000'
    i = int(i)
    for datas in data:
      dt = datas['date_joined'].date().strftime("%Y%m%d")
      if dt == now:
         i = i+1
      else:
          i = now+'001'
          i = int(i)
    return i