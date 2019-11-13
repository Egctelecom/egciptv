from django.conf.urls import url
from crmadmin.views import others_settings_of_frontend

urlpatterns = [
	
	url(r'^others/details/index/$', others_settings_of_frontend.index_others_details, name='index_others_details'),
	url(r'^others/details/add/$', others_settings_of_frontend.add_others_details, name='add_others_details'),
	url(r'^others/details/edit/(?P<id>[0-9]+)$', others_settings_of_frontend.edit_others_details, name='edit_others_details'),
	
]

