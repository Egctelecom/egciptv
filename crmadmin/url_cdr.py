from django.conf.urls import url
from crmadmin.views import cdr_records as  cdr_records_views
urlpatterns = [

url(r'^cdr_details/$', cdr_records_views.cdr_details, name='cdr_details'),
url(r'^cdr_filter/$', cdr_records_views.cdr_date_filter_details, name='cdr_filter'),

]