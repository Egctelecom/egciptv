from django.conf.urls import url, include
from sitefrontendbyadmin.views import views

urlpatterns = [
	
	url(r'^menu/parent/category/list/$', views.menu_parent_category_list, name='menu_parent_category_list'),
	url(r'^menu/list/parent/category/add/  $', views.menu_parent_category_add, name='menu_parent_category_add'),
	url(r'^menu/list/parent/category/edit/(?P<id>[0-9]+)$', views.menu_parent_category_edit, name='menu_parent_category_edit'),
	
	
    url(r'^menu/parent/sub/category/list/$', views.menu_parent_sub_category_list, name='menu_parent_sub_category_list'),
	url(r'^menu/list/parent/sub/category/add/  $', views.menu_parent_sub_category_add, name='menu_parent_sub_category_add'),
	url(r'^menu/list/parent/sub/category/edit/(?P<id>[0-9]+)$', views.menu_sub_parent_category_edit, name='menu_parent_sub_category_edit'),
	
	
    url(r'^menu/category/list/$', views.menu_category_list, name='menu_category_list'),
	url(r'^menu/category/add/$', views.menu_category_add, name='menu_category_add'),
	url(r'^menu/category/edit/(?P<id>[0-9]+)$', views.menu_category_edit, name='menu_category_edit'),
	
	url(r'^get_sub_parent_list/$', views.get_sub_parent_list, name='get_sub_parent_list'),
			
    url(r'^service/features/list/$', views.service_feature_list, name='service_feature_list'),
	url(r'^service/features/add/$', views.service_feature_add, name='service_feature_add'),
	url(r'^service/features/edit/(?P<id>[0-9]+)$', views.service_feature_edit, name='service_feature_edit'),
	
	
	# Slider
	
	url(r'^slider/list/$', views.slider_index, name='slider_index'),
	url(r'^slider/add/$', views.slider_add, name='slider_add'),
	url(r'^slider/edit/(?P<id>[0-9]+)$', views.slider_edit, name='slider_edit'),
	url(r'^slider/delete/(?P<id>[0-9]+)$', views.slider_delete, name='slider_delete'),
	
	# Network Status
	
    url(r'^network_status/list/$', views.network_status_index, name='network_status_index'),
	url(r'^network_status/add/$', views.network_status_add, name='network_status_add'),
	url(r'^network_status/edit/(?P<id>[0-9]+)$', views.network_status_edit, name='network_status_edit'),
	url(r'^network_status/delete/(?P<id>[0-9]+)$', views.network_status_delete, name='network_status_delete'),
	
	# Network Status
	
	url(r'^faq/list/$', views.faq_index, name='faq_index'),
	url(r'^faq/add/$', views.faq_add, name='faq_add'),
	url(r'^faq/edit/(?P<id>[0-9]+)$', views.faq_edit, name='faq_edit'),
	url(r'^faq/delete/(?P<id>[0-9]+)$', views.faq_delete, name='faq_delete'),
	
	
	# Follow Us
	
	url(r'^follow_us/list/$', views.follow_us_index, name='follow_us_index'),
	url(r'^follow_us/add/$', views.follow_us_add, name='follow_us_add'),
	url(r'^follow_us/edit/(?P<id>[0-9]+)$', views.follow_us_edit, name='follow_us_edit'),
	url(r'^follow_us/delete/(?P<id>[0-9]+)$', views.follow_us_delete, name='follow_us_delete'),
	
	# Logo
	
	url(r'^logo/$', views.logo_index, name='logo'),
	url(r'^logo/add/$', views.upload_logo_area, name='upload_logo_area'),
	url(r'^logo/edit/(?P<id>[0-9]+)$', views.edit_logo_area, name='edit_logo_area'),

	# Background Image
	url(r'^bg_image/$', views.background_list, name='bg_image_list'),
	url(r'^bg_image/add/$', views.background_add, name='bg_image_add'),
	url(r'^bg_image/edit/(?P<id>[0-9]+)$', views.background_edit, name='bg_image_edit'),
	url(r'^bg_image/delete/(?P<id>[0-9]+)$', views.edit_logo_area, name='bg_image_delete'),

]