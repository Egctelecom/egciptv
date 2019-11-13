from django.conf.urls import url
from crmadmin.views import service_views as  services_views
urlpatterns = [

url(r'^Services/$', services_views.services_index, name='services'),
url(r'^Services/Add/$', services_views.services_add, name='services_add'),
url(r'^Services/Delete/(?P<pk>[0-9]+)$', services_views.services_delete, name='services_delete'),
url(r'^Services/Edit/(?P<pk>[0-9]+)$', services_views.services_edit, name='services_edit'),

]
