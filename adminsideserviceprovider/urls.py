from django.conf.urls import url
from . import views as service_provider_views

urlpatterns = [

#================================================== Service Provider ====================================================

url(r'^Service/Provider/$', service_provider_views.service_provider_index, name='service_provider_index'),
url(r'^Service/Provider/Add/$', service_provider_views.service_provider_add, name='service_provider_add'),
url(r'^Service/Provider/Edit/(?P<id>[0-9]+)$', service_provider_views.service_provider_edit, name='service_provider_edit'),

url(r'^service/provider/plan/add/(?P<id>[0-9]+)$', service_provider_views.plan_add_to_service_provider, name='plan_add_to_service_provider'),
url(r'^service/provider/plan/all/(?P<id>[0-9]+)$', service_provider_views.view_plan_of_service_provider, name='view_plan_of_service_provider'),
url(r'^service/provider/special_offer/plan/add/(?P<id>[0-9]+)$', service_provider_views.plan_add_special_offer_to_service_provider, name='plan_add_special_offer_to_service_provider'),
url(r'^service/provider/special_offer/plan/all/(?P<id>[0-9]+)$', service_provider_views.view_special_offer_plan_of_service_provider, name='view_special_offer_plan_of_service_provider'),
url(r'^service/provider/plan/edit/(?P<id>[0-9]+)$', service_provider_views.plan_edit, name='plan_edit'),

#================================================== Service Provider With City Map ====================================================

url(r'^Service/ProviderCityMap/$', service_provider_views.service_provider_with_city_index, name='service_provider_with_city_index'),
# url(r'^Service/ProviderCityMap/Edit/(?P<id>[0-9]+)$', service_provider_views.service_provide_with_city_edit, name='service_provider_with_city_edit'),

url(r'^service/province_with_city/(?P<id>[0-9]+)$', service_provider_views.province_with_city, name='province_with_city'),
url(r'^SetServiceProvider/(?P<id>[0-9]+)$', service_provider_views.set_service_provider, name='set_service_provider'),
url(r'^SaveServiceProviderToCity/$', service_provider_views.save_service_provider_to_city, name='save_service_provider_to_city'),

url(r'^get-service-category/$', service_provider_views.get_service_via_category, name='get_service_via_category'),
url(r'^get-service-special-offer-category/$', service_provider_views.get_service_special_offer_via_category, name='get_service_special_offer_via_category'),
url(r'^get-service-name/$', service_provider_views.get_service_name, name='get_service_name'),
url(r'^get-service-special-offers-name/$', service_provider_views.get_special_offer_service_name, name='get_special_offer_service_name'),

#================================================== Add Hardware According to data plan ================================================

url(r'^service/provider/plan/view-hardware/(?P<id>[0-9]+)$', service_provider_views.view_hw_in_service_provider, name='view_hw_in_service_provider'),
url(r'^service/provider/plan/add-hardware/(?P<id>[0-9]+)$', service_provider_views.add_hw_in_service_provider, name='add_hw_in_service_provider'),
url(r'^service/provider/plan/edit-hardware/(?P<id>[0-9]+)$', service_provider_views.edit_hw_in_service_provider, name='edit_hw_in_service_provider'),
url(r'^service/provider/plan/delete-hardware/(?P<id>[0-9]+)$', service_provider_views.delete_hw_in_service_provider, name='delete_hw_in_service_provider'),


url(r'^hardware/add/$', service_provider_views.add_hw_list, name='add_hw_list'),
url(r'^hardware/edit/(?P<id>[0-9]+)$', service_provider_views.edit_hw_list, name='edit_hw_list'),
url(r'^hardware/view/$', service_provider_views.view_hw_list, name='view_hw_list'),
url(r'^hardware/view/$', service_provider_views.view_hw_list, name='view_hw_list'),

#================================================== Ticket ================================================

url(r'^ticket/view/$', service_provider_views.ticket_index, name='ticket_index'),
url(r'^ticket/add/$', service_provider_views.ticket_add, name='ticket_add'),
url(r'^ticket/edit/(?P<pk>[0-9]+)$', service_provider_views.ticket_edit, name='ticket_edit'),
url(r'^ticket/delete/(?P<pk>[0-9]+)$', service_provider_views.ticket_delete, name='ticket_delete'),


#================================================= Map ticket With Service Provide =======================

url(r'^ticket/service_provider/add/$', service_provider_views.add_map_ticket_with_service_provider, name='add_map_ticket_with_service_provider'),
url(r'^ticket/service_provider/customer/update/(?P<pk>[0-9]+)$', service_provider_views.update_customer_ticket, name='update_customer_ticket'),
url(r'^ticket/service_provider/customer/update/data$', service_provider_views.update_customer_ticket_data, name='update_customer_ticket_data'),



]