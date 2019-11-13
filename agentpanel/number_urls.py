from django.conf.urls import url
from agentpanel.views import number_provider_views as number_views

urlpatterns = [

url(r'^number/$', number_views.index, name='agent_number'),
url(r'^number/add/$', number_views.add, name='agent_number_add'),
url(r'^number/ratecenters/$', number_views.get_ratecenters, name='agent_get_ratecenters'),
url(r'^number/province/$', number_views.get_province_via , name='agent_get_province_via'),
url(r'^number/did/$', number_views.get_number , name='agent_get_number'),
#========================================================================== Add Number ====================================

url(r'^number/maptouser/(?P<id>[0-9]+)$', number_views.map_number_to_user , name='agent_map_number_to_user'),

]