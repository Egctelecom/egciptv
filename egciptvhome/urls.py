from django.conf.urls import url
from egciptvhome.views import views as custome_view , plans , registration
from crmadmin.views import special_offers,special_offers_category
urlpatterns = [
	url(r'^$', custome_view.index, name='home'),
	url(r'^login$', custome_view.customer_login, name='login'),
	url(r'^my_account/(?P<pk>[0-9]+)$', custome_view.my_account, name='my_account'),
	url(r'^logout', custome_view.user_logout, name='logout'),
	url(r'^contact_us$', custome_view.contact_us, name='contact_us'),
	url(r'^other_service$', custome_view.other_services, name='other_service'),
	
	url(r'^send_contact_to_admin$', custome_view.send_contact_to_admin, name='send_contact_to_admin'),
	
	#=============================== Province ====================================#
	
	
    url(r'^get_city_of_region$', custome_view.get_city_of_region, name='get_city_of_region'),
	
    url(r'^get_city_according_region$', custome_view.get_city_according_region, name='get_city_according_region'),
    url(r'^reg/get_city/region$', custome_view.reg_get_city_according_region, name='reg_get_city_according_region'),
    url(r'^reg/get_city/billing/region$', custome_view.reg_billing_get_city_according_region, name='reg_billing_get_city_according_region'),
	
	
    url(r'^special_offers/get_city/region$', custome_view.special_offers_get_city_according_region, name='special_offers_get_city_according_region'),
    url(r'^special_offers/get_city/billing/region$', custome_view.special_offers_billing_get_city_according_region, name='special_offers_billing_get_city_according_region'),
  
    url(r'^check_session$', custome_view.check_session, name='check_session'),
    url(r'^set_lang_session$', custome_view.set_lang_session, name='set_lang_session'),
	
	#==============================  Plan =========================================#
	
    url(r'^plans/(?P<parent_id>\d+)/(?P<sub_parent_id>\d+)/(?P<category_id>\d+)$', plans.plans_according_city, name='plans_according_city'),
    url(r'^special/offers/plans/lists/(?P<pk>[0-9]+)$', plans.special_offers_plans_lists, name='special_offers_plans_lists'),
    url(r'^special/offers_plans/details/(?P<id>\d+)$', plans.special_offers_plans_details, name='special_offers_plans_details'),

    # Plans Details
	
	url(r'^plans/details/(?P<menu_id>\d+)/(?P<service_id>\d+)/(?P<type>[a-z]+)$',
	    plans.plans_details, name='plans_details'),
	
	# ==============================  Apply For Registrations =========================================#
	
	url(r'^plans/apply_for_registrations/(?P<menu_id>\d+)/(?P<service_id>\d+)/(?P<type>[a-z]+)$', registration.apply_for_registration,name='apply_for_registration'),

	
	url(r'^plans/apply_for_registrations_special_offers/(?P<id>\d+)$', registration.apply_for_registrations_special_offers,name='apply_for_registrations_special_offers'),
	
	url(r'^details/special_offers/(?P<type_name>[\w ]+)/(?P<combo_name>[\w ]+)/(?P<parent_id>[0-9]+)/(?P<sub_parent_id>[0-9]+)$',special_offers_category.get_details_of_special_offers, name='get_details_of_special_offers'),
	url(r'^brief/details/special_offers/(?P<id>[0-9]+)$', special_offers_category.get_special_offers_plan_details,
	    name='get_special_offers_plan_details'),
	
	url(r'^service/features/details/(?P<pk>\d+)$', custome_view.details,name='service_features_details'),
	
	
	# ============================== Network Status ==============================
	
    url(r'^network/status/$', custome_view.network_status, name='network_status'),
	
	#============================== FAQs ==============================
	
    url(r'^faq/$', custome_view.faq, name='faq'),
	
	#============================== About Us ==============================
	
    url(r'^about_us/$', custome_view.about_us, name='about_us'),
   
    #============================== Terms and Conditions ==============================
	
    url(r'^termsandconditions/$', custome_view.termsandconditions, name='termsandconditions'),
	
    url(r'^privacyandpolicy/$', custome_view.privacyandpolicy, name='privacyandpolicy'),
	
	
    url(r'^voip_long_distance_rate/$', custome_view.voip_rate, name='voip_rate'),
	


]