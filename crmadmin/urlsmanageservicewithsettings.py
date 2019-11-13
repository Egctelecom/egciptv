from django.conf.urls import url

from crmadmin.views import settings_manageservicewithviews as  settings_views

urlpatterns = [
#==========================================================MANAGE SERVICE WITH CATEGORY ===============================#

url(r'^Settings/ManageServicePrice/ServicePriceCategory/Update/(?P<pk>[0-9]+)$', settings_views.settings_manage_service_price_category_edit,name='settings_manage_service_price_category_edit'),
url(r'^Settings/ManageServicePrice/ServicePriceCategory/Delete/(?P<pk>[0-9]+)$', settings_views.settings_manage_service_price_category_delete,name='settings_manage_service_price_category_delete'),
url(r'^Settings/ManageServicePrice/ServicePriceCategory/Add/$', settings_views.settings_manage_service_price_category_add,name='settings_manage_service_price_category_add'),

#==========================================================MANAGE SERVICE  ===============================#

url(r'^Settings/ManageServicePrice/ServicePrice/Edit/(?P<pk>[0-9]+)/(?P<category_id>[0-9]+)$', settings_views.settings_manage_service_price_edit,name='settings_manage_service_price_edit'),
url(r'^Settings/ManageServicePrice/ServicePrice/Add/(?P<category_id>[0-9]+)$', settings_views.settings_manage_service_price_add,name='settings_manage_service_price_add'),
url(r'^Settings/ManageServicePrice/ServicePrice/Delete/(?P<pk>[0-9]+)$', settings_views.settings_manage_service_price_delete,name='settings_manage_service_price_delete'),

url(r'^Settings/ManageServicePrice/ServicePrice/Price/Updatesettings_manage_service_price_edit$', settings_views.settings_manage_service_price_value_update,name='settings_manage_service_price_value_update'),

url(r'^Settings/ManageServicePrice/serviceprice/price/settings/document/upload/(?P<id>[0-9]+)$', settings_views.settings_manage_service_price_doc_add,name='settings_manage_service_price_doc_add'),
url(r'^Settings/ManageServicePrice/serviceprice/price/settings/document/view/(?P<id>[0-9]+)$', settings_views.settings_manage_service_price_doc_view,name='settings_manage_service_price_doc_view'),
url(r'^Settings/ManageServicePrice/serviceprice/price/settings/document/delete/(?P<id>[0-9]+)/(?P<service_provider_id>[0-9]+)$', settings_views.settings_manage_service_price_doc_delete,name='settings_manage_service_price_doc_delete'),
url(r'^Settings/ManageServicePrice/serviceprice/price/settings/document/change$', settings_views.settings_manage_service_price_doc_status_change,name='settings_manage_service_price_doc_status_change'),



#============================================================ SET TAB ========================================#
url(r'^set_tab/$',settings_views.set_tab,name='set_tab'),
url(r'^set_tab_col/$',settings_views.set_tab_col,name='set_tab_col'),

]
