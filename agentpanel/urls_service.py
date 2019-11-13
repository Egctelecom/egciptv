from django.conf.urls import url
from agentpanel.views import service_views as  services_views
urlpatterns = [

url(r'^Services/$', services_views.services_index, name='agent_services'),
url(r'^Services/Add/$', services_views.services_add, name='agent_services_add'),
url(r'^Services/Delete/(?P<pk>[0-9]+)$', services_views.services_delete, name='agent_services_delete'),
url(r'^Services/Edit/(?P<pk>[0-9]+)$', services_views.services_edit, name='agent_services_edit'),

]
