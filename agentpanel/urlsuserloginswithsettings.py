from django.conf.urls import url

from agentpanel.views import settings_loginsviews as  settings_views

urlpatterns = [
#========================================================== User Logins ===============================#

# url(r'^Settings/ManageServicePrice/ServicePriceCategory/Delete/(?P<pk>[0-9]+)$', settings_views.settings_manage_service_price_category_delete,name='settings_manage_service_price_category_delete'),
url(r'^Settings/Logins/$', settings_views.settings_logins_add,name='agent_settings_logins_add'),
url(r'^Settings/Logins/Update/(?P<pk>[0-9]+)$', settings_views.settings_logins_edit,name='agent_settings_logins_edit'),



]
