from django.conf.urls import url
from crmadmin.views import special_offers,special_offers_category
urlpatterns = [

	#==============================  Special Offers ==================================================#
	
	url(r'^special/offers/$', special_offers.index, name='special_offers'),
	url(r'^special/offers/add$', special_offers.special_offers_services_plan_add, name='special_offers_services_plan_add'),
    url(r'^special/offers/edit/(?P<pk>[0-9]+)$', special_offers.special_offers_services_plan_edit, name='special_offers_services_plan_edit'),
	url(r'^special/offers/plans/(?P<pk>[0-9]+)$', special_offers.special_offers_services_plan, name='special_offers_services_plan'),
	url(r'^special/offers/plans/hardwares/(?P<pk>[0-9]+)/(?P<special_offers_id>[0-9]+)$', special_offers.special_offers_services_plan_hardware, name='special_offers_services_plan_hardware'),
	
	
	url(r'^special/offers/offers_price/add/(?P<pk>[0-9]+)/(?P<special_offers_id>[0-9]+)/(?P<service_plan_id>[0-9]+)/(?P<service_price_id>[0-9]+)$', special_offers.special_offers_services_plan_hardware_offer_price_add,
	    name='special_offers_services_plan_hardware_offer_price'),
    url(r'^special/offers/offers_price/editorview/(?P<pk>[0-9]+)/(?P<special_offers_id>[0-9]+)/(?P<service_plan_id>[0-9]+)/(?P<service_price_id>[0-9]+)$', special_offers.special_offers_services_plan_hardware_offer_price_editorview,
	    name='editorview_special_offers_services_plan_hardware_offer_price'),
	
	url(r'^special/offers/document/upload/(?P<id>[0-9]+)$', special_offers.special_offers_doc_add,
	    name='special_offers_doc_add'),
	url(r'^special/offers/document/view/(?P<id>[0-9]+)$', special_offers.special_offers_doc_view,
	    name='special_offers_doc_view'),
    url(r'^special/offers/document/delete/(?P<id>[0-9]+)/(?P<special_offers_id>[0-9]+)$', special_offers.special_offers_doc_delete,
	    name='special_offers_doc_delete'),
    url(r'^special/offers/document/status/change$', special_offers.special_offers_doc_status_change,
	    name='special_offers_doc_status_change'),
	
	# ==============================  Special Offers Categories =========================================#
	
	url(r'^special/offers/parent/category/list/$', special_offers_category.special_offers_parent_category_list, name='special_offers_parent_category_list'),
	url(r'^special/offers/list/parent/category/add/  $', special_offers_category.special_offers_parent_category_add, name='special_offers_parent_category_add'),
	url(r'^special/offers/list/parent/category/edit/(?P<id>[0-9]+)$', special_offers_category.special_offers_parent_category_edit,name='special_offers_parent_category_edit'),
	
	url(r'^special/offers/parent/sub/category/list/$', special_offers_category.special_offers_parent_sub_category_list, name='special_offers_parent_sub_category_list'),
	url(r'^special/offers/list/parent/sub/category/add/$', special_offers_category.special_offers_parent_sub_category_add,name='special_offers_parent_sub_category_add'),
	url(r'^special/offers/list/parent/sub/category/edit/(?P<id>[0-9]+)$', special_offers_category.special_offers_sub_parent_category_edit,name='special_offers_parent_sub_category_edit'),
	
	url(r'^special/offers/category/list/$', special_offers_category.special_offers_category_list, name='special_offers_category_list'),
	url(r'^special/offers/category/add/$', special_offers_category.special_offers_category_add, name='special_offers_category_add'),
	url(r'^special/offers/category/edit/(?P<id>[0-9]+)$', special_offers_category.special_offers_category_edit, name='special_offers_category_edit'),
	
	url(r'^special/offers/category/delete/(?P<id>[0-9]+)$', special_offers_category.special_offers_category_delete, name='special_offers_category_delete'),
	
	
	url(r'^special/offers/sub/parent/category/list/$', special_offers_category.get_sub_special_offers_parent_list, name='get_sub_special_offers_parent_list'),
	
	url(r'^get_city/$', special_offers_category.get_city, name='get_city'),
	
	url(r'^get_set_of_special_offers/$', special_offers_category.get_set_of_special_offers, name='get_set_of_special_offers'),
	url(r'^get_data_according_to_type/$', special_offers_category.get_data_according_to_type, name='get_data_according_to_type'),

	
	

]

