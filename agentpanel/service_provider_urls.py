from django.conf.urls import url
from agentpanel.views import service_provider_views as service_provider_views

urlpatterns = [

#================================================== Service Provider ====================================================================================

url(r'^Service/Provider/$', service_provider_views.service_provider_index, name='agent_service_provider_index'),
url(r'^Service/Provider/Add/$', service_provider_views.service_provider_add, name='agent_service_provider_add'),
url(r'^Service/Provider/Edit/(?P<id>[0-9]+)$', service_provider_views.service_provider_edit, name='agent_service_provider_edit'),

url(r'^service/provider/plan/add/(?P<id>[0-9]+)$', service_provider_views.plan_add_to_service_provider, name='agent_plan_add_to_service_provider'),
url(r'^service/provider/plan/all/(?P<id>[0-9]+)$', service_provider_views.view_plan_of_service_provider, name='agent_view_plan_of_service_provider'),
url(r'^service/provider/plan/edit/(?P<id>[0-9]+)$', service_provider_views.plan_edit, name='agent_plan_edit'),

#================================================== Service Provider With City Map ======================================================================

url(r'^Service/ProviderCityMap/$', service_provider_views.service_provider_with_city_index, name='agent_service_provider_with_city_index'),
# url(r'^Service/ProviderCityMap/Edit/(?P<id>[0-9]+)$', service_provider_views.service_provide_with_city_edit, name='service_provider_with_city_edit'),

url(r'^service/province_with_city/(?P<id>[0-9]+)$', service_provider_views.province_with_city, name='agent_province_with_city'),
url(r'^SetServiceProvider/(?P<id>[0-9]+)$', service_provider_views.set_service_provider, name='agent_set_service_provider'),
url(r'^SaveServiceProviderToCity/$', service_provider_views.save_service_provider_to_city, name='agent_save_service_provider_to_city'),

url(r'^get-service-category/$', service_provider_views.get_service_via_category, name='agent_get_service_via_category'),
url(r'^get-service-name/$', service_provider_views.get_service_name, name='agent_get_service_name'),

#================================================== Add Hardware According to data plan ==================================================================

url(r'^service/provider/plan/view-hardware/(?P<id>[0-9]+)$', service_provider_views.view_hw_in_service_provider, name='agent_view_hw_in_service_provider'),
url(r'^service/provider/plan/add-hardware/(?P<id>[0-9]+)$', service_provider_views.add_hw_in_service_provider, name='agent_add_hw_in_service_provider'),
url(r'^service/provider/plan/edit-hardware/(?P<id>[0-9]+)$', service_provider_views.edit_hw_in_service_provider, name='agent_edit_hw_in_service_provider'),
url(r'^service/provider/plan/delete-hardware/(?P<id>[0-9]+)$', service_provider_views.delete_hw_in_service_provider, name='agent_delete_hw_in_service_provider'),


url(r'^hardware/add/$', service_provider_views.add_hw_list, name='agent_add_hw_list'),
url(r'^hardware/edit/(?P<id>[0-9]+)$', service_provider_views.edit_hw_list, name='agent_edit_hw_list'),
url(r'^hardware/view/$', service_provider_views.view_hw_list, name='agent_view_hw_list'),


]