from django.conf.urls import url
from agentpanel.views import settings_views as  settings_views

urlpatterns = [

url(r'^Settings/$', settings_views.settings, name='agent_settings'),

]