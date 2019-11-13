from django.conf.urls import url
from . import views as number_views

urlpatterns = [

url(r'^number/$', number_views.index, name='number'),
url(r'^number/add/$', number_views.add, name='number_add'),
url(r'^number/ratecenters/$', number_views.get_ratecenters, name='get_ratecenters'),
url(r'^number/province/$', number_views.get_province_via , name='get_province_via'),
url(r'^number/did/$', number_views.get_number , name='get_number'),
#========================================================================== Add Number ====================================

url(r'^number/maptouser/(?P<id>[0-9]+)$', number_views.map_number_to_user , name='map_number_to_user'),

]