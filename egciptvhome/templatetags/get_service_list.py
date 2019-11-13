from random import randint
from adminsidecustomer.models import Country,Province
from adminsideserviceprovider.models import ServiceProvider
from adminsideserviceprovider.models import ServiceProvider, ServiceProviderPlan
from sitefrontendbyadmin.models import MenuSubParentCategory,MenuCategory,MenuParentCategory,Followus
from django import template
from egciptvhome.models import Otherdetails
register = template.Library()


@register.simple_tag()
def get_service_category_list(pk):
	services_provider_with_plan = ServiceProviderPlan.objects.values(
		'id',
		'service_provider_id__service_provider_name',
		'service_provider_id',
		'title',
		'retail',
		'actual',
		'qty'
	).filter(service_provider_id=pk)
	
	return services_provider_with_plan

@register.simple_tag()
def get_service_category_data():
	parent_category = MenuParentCategory.objects.values('id', 'service_parent_category_name').filter(status='active').distinct('service_parent_category_name')
	return parent_category
	
@register.simple_tag()
def get_sub_service_category_list(id):
	menu = MenuSubParentCategory.objects.values('id', 'service_parent_category_id','service_sub_parent_category_name').filter(service_parent_category_id=id,status='active').distinct('service_sub_parent_category_name')
	return menu


@register.simple_tag()
def get_service_category_menu_list(id,parent_id):
	
	menu_list = MenuCategory.objects.values('id',
	                                        'service_parent_category_id',
	                                        'service_category_id__service_category_name',
	                                        'service_parent_category_id__service_parent_category_name',
	                                        'service_sub_parent_category_name_id',
	                                        'service_category_id',
	                                        'status',
	                                        'service_sub_parent_category_name_id__service_sub_parent_category_name').filter(service_sub_parent_category_name_id=id,
	                                                                                                                        service_parent_category_id=parent_id,status='active')
	

	return menu_list


@register.simple_tag()
def get_menu_data(id):
	menu_list = MenuCategory.objects.values('id',
	                                        'service_parent_category_id',
	                                        'service_category_id__service_category_name',
	                                        'service_parent_category_id__service_parent_category_name',
	                                        'service_sub_parent_category_name_id',
	                                        'service_category_id',
	                                        'status',
	                                        'service_sub_parent_category_name_id__service_sub_parent_category_name').filter(pk=id,status='active')
	
	return menu_list


@register.simple_tag()
def get_plan_data(id):
	service_list = ServiceProviderPlan.objects.values('title', 'retail', 'actual', 'qty',
                                                  'manage_service_id__service_desc').filter(pk=id,manage_service_id__special_offer='no')
	
	return service_list

@register.simple_tag()
def get_contact():
	other_details = Otherdetails.objects.values('id',
	                                            'key',
	                                            'value',
	                                            'address',
	                                            'country',
	                                            'city',
	                                            'province',
	                                            'zip',
	                                            'fax',
	                                            'phone',
	                                            'email').filter(key='Contact')
	return other_details


@register.simple_tag()
def get_about():
	other_details = Otherdetails.objects.values('id',
	                                            'key',
	                                            'value').filter(key='About')
	return other_details


@register.simple_tag()
def follow_us_function():
	follow_us = Followus.objects.values('id', 'url', 'fa_fa_icon', 'status').filter(status='active')
	return follow_us