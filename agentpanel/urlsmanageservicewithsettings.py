from django.conf.urls import url

from agentpanel.views import settings_manageservicewithviews as  settings_views

urlpatterns = [
#==========================================================MANAGE SERVICE WITH CATEGORY ===============================#

url(r'^Settings/ManageServicePrice/ServicePriceCategory/Update/(?P<pk>[0-9]+)$', settings_views.settings_manage_service_price_category_edit,name='agent_settings_manage_service_price_category_edit'),
url(r'^Settings/ManageServicePrice/ServicePriceCategory/Delete/(?P<pk>[0-9]+)$', settings_views.settings_manage_service_price_category_delete,name='agent_settings_manage_service_price_category_delete'),
url(r'^Settings/ManageServicePrice/ServicePriceCategory/Add/$', settings_views.settings_manage_service_price_category_add,name='agent_settings_manage_service_price_category_add'),

#==========================================================MANAGE SERVICE  ===============================#

url(r'^Settings/ManageServicePrice/ServicePrice/Edit/(?P<pk>[0-9]+)/(?P<category_id>[0-9]+)$', settings_views.settings_manage_service_price_edit,name='agent_settings_manage_service_price_edit'),
url(r'^Settings/ManageServicePrice/ServicePrice/Add/(?P<category_id>[0-9]+)$', settings_views.settings_manage_service_price_add,name='agent_settings_manage_service_price_add'),
url(r'^Settings/ManageServicePrice/ServicePrice/Delete/(?P<pk>[0-9]+)$', settings_views.settings_manage_service_price_delete,name='agent_settings_manage_service_price_delete'),

url(r'^Settings/ManageServicePrice/ServicePrice/Price/Updatesettings_manage_service_price_edit$', settings_views.settings_manage_service_price_value_update,name='agent_settings_manage_service_price_value_update'),

#============================================================ SET TAB ========================================#
url(r'^set_tab/$',settings_views.set_tab,name='agent_set_tab'),
url(r'^set_tab_col/$',settings_views.set_tab_col,name='agent_set_tab_col'),

]
