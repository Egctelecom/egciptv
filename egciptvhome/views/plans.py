from django.shortcuts import render
from sitefrontendbyadmin.models import MenuParentCategory,MenuCategory,MenuSubParentCategory,SpecialoffersUnderCategory
from adminsideserviceprovider.models import ServiceProviderPlan,ServiceProviderCityMap
from sitefrontendbyadmin.models import SpecialOffers
from django.http import *
from django.urls import reverse



def plans_according_city(request,parent_id,sub_parent_id,category_id):
	
	if request.method=='GET':
		
		parent_categories = MenuParentCategory.objects.values('service_parent_category_name','id').filter(pk=parent_id)
		sub_parent_categories = MenuSubParentCategory.objects.values('service_parent_category_id','service_sub_parent_category_name','id').filter(pk=sub_parent_id)
		category = MenuCategory.objects.values('service_category_id__service_category_name','service_parent_category_id','service_sub_parent_category_name_id','id').filter(service_category_id=category_id)
		
		if 'city_id' not in request.session:
			
			return HttpResponseRedirect(reverse('home'))
		
		else:
			
			
			country_province_city = ServiceProviderCityMap.objects.values('service_provider_id').filter(city_id=request.session['city_id'],
			                                                                                            province_id=request.session['province_id'],
			                                                                                            country_id=request.session['country_id'])
			
					
			rt=[]
			rate=[]
			
			for ct in country_province_city:
			
				service_list = ServiceProviderPlan.objects.values('id',
				                                                  'title',
				                                                  'retail',
				                                                  'actual',
				                                                  'qty',
				                                                  'manage_service_id__service_desc',
				                                                  'manage_service_id',
				                                                  'manage_service_id__service_logo').filter(manage_service_category_id=category_id,
				                                                                                            manage_service_id__special_offer='no',status='active',
				                                                                                            service_provider_id=ct['service_provider_id']).distinct('title','service_provider_id')
				
				
				rt.append(service_list)
	
			range = len(rt)
			if range:
				flag=1
			else:
				flag=0
			return render(request, 'egciptv/plans/index.html',{'parent_categories':parent_categories,'sub_parent_categories':sub_parent_categories,'category':category,'service_list':rt,'type':'normal','range':range,'flag':flag})
		


# Special Offers Plans List
def special_offers_plans_lists(request,pk):
	special_offers_plans_list = SpecialoffersUnderCategory.objects.values('id',
	                                                                'special_offers_id',
	                                                                'special_offers_parent_category_id',
	                                                                'special_offers_sub_parent_category_id',
	                                                                'special_offers_parent_category_id__special_offers_parent_category_name',
	                                                                'special_offers_sub_parent_category_id__special_offers_sub_parent_category_name',
	                                                                'special_offers_id__details',
	                                                                'telecom_name',
	                                                                'telecom_logo',
	                                                                'special_offers_id__features',
	                                                                'special_offers_id__offers_price',
	                                                                'special_offers_id__actual_price',
	                                                                'status').filter(special_offers_sub_parent_category_id=pk,status='active')
	
	return render(request, 'egciptv/special_offers/plans.html', {'special_offers_plans_list': special_offers_plans_list})
	
# Perticular Special Offers Plans Details
def special_offers_plans_details(request,id):
	if request.method == 'GET':
		special_offers_list = SpecialoffersUnderCategory.objects.values('id',
		                                                                'special_offers_id',
		                                                                'special_offers_parent_category_id',
		                                                                'special_offers_sub_parent_category_id',
		                                                                'special_offers_parent_category_id__special_offers_parent_category_name',
		                                                                'special_offers_sub_parent_category_id__special_offers_sub_parent_category_name',
		                                                                'special_offers_id__details',
		                                                                'telecom_name',
		                                                                'telecom_logo',
		                                                                'special_offers_id__features',
		                                                                'special_offers_id__offers_price',
		                                                                'special_offers_id__actual_price',
		                                                                'status').filter(pk=id,status='active')
		
		
	    
		
		return render(request, 'egciptv/special_offers/index.html',{'special_offers_list':special_offers_list})


def plans_details(request,menu_id,service_id,type):
	if request.method == 'GET':
		service_list = ServiceProviderPlan.objects.values('id','title','retail','actual','qty','manage_service_id__service_desc','manage_service_id').filter(id=service_id)
		return render(request, 'egciptv/plans/details.html',{'service_list':service_list,'type':type,'menu_id':menu_id})

		
	