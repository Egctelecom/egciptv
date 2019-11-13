from django.conf.urls import url
from crmadmin.views import agent as  agent_views,agent_permission
urlpatterns = [

url(r'^agent/$', agent_views.agent_index, name='agent'),
url(r'^agent/add/$', agent_views.add_agent, name='agent_add'),
url(r'^agent/edit/(?P<pk>[0-9]+)$', agent_views.edit_agent, name='agent_edit'),
url(r'^agent/delete/(?P<pk>[0-9]+)$', agent_views.delete_agent, name='agent_delete'),

url(r'^agent/permission/(?P<pk>[0-9]+)$', agent_permission.agent_index, name='agent_permission'),
url(r'^agent/set/permission/$', agent_permission.save_permission_to_agent, name='save_permission_to_agent'),

]
