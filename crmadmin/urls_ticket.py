from django.conf.urls import url
from crmadmin.views import ticket as  ticket_views

urlpatterns = [

url(r'^ticket/list/$', ticket_views.ticket_list, name='tickets_list'),

]