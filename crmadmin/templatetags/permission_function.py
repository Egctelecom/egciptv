from django import template
from django.contrib.auth.models import User

register = template.Library()


#============================================== PERMISSION CHECKING ====================================================


@register.simple_tag()
def get_permission(codename,haveperm,user_id):
    for havePerm in haveperm:
     data = havePerm.split('.')
     if data[1] == codename:
       u = User.objects.get(pk=user_id)
       perm = u.has_perm(data[0]+'.'+data[1])
       return perm
