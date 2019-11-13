from django import template
from crmadmin.models import ManageServicesPriceCategory, ManageServicePrice
from sitefrontendbyadmin.models import SpecialoffersUnderCategory,WebLogo,SpecialOffersPlanswithHardwareRates,SpecialoffersSubParentCategory,SpecialoffersParentCategory,SpecialOffers,SpecialOffersPlanswithHardwareRates
from adminsideserviceprovider.models import ServiceProviderPlan
from adminsidecustomer.models import Country,Province,City
register = template.Library()


@register.simple_tag()
def get_service_each_category_special_offer_price(pk):
    servies = ManageServicePrice.objects.values('id',
                                                'service_category_id',
                                                'service_name',
                                                'service_price',
                                                'service_desc',
                                                'status').filter(service_category_id=pk,special_offer='yes')
    return servies

# Special Offers
@register.simple_tag()
def special_offers_function(pk):
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
                                                                    'status').filter(special_offers_sub_parent_category_id=pk)
    return special_offers_list
   


   
# Special Offers Hardwares
@register.simple_tag()
def special_offers_plans_with_hardwareRates_function(id):
    sp = SpecialOffersPlanswithHardwareRates.objects.values('id','hw_id','hw_id__hw_title','hw_qty','device_buy','device_rental','montly_rent','offer_price').filter(special_offers_id=id)
    return sp

#Service Details
@register.simple_tag()
def special_service_details(pk):
    special_offers = ServiceProviderPlan.objects.values('id',
                                                        'title',
                                                        'retail',
                                                        'actual',
                                                        'qty',
                                                        'manage_service_id',
                                                        'manage_service_id__service_desc').filter(manage_service_id=pk,manage_service_id__special_offer='yes').distinct('title')
    return special_offers


#Special Offers Parent category
@register.simple_tag()
def get_parent_category():
    special_offers_parent_cate = SpecialoffersParentCategory.objects.values('id','special_offers_parent_category_name','desc').filter(status='active')
    return  special_offers_parent_cate

#Special Offers Sub Parent under Parent category
@register.simple_tag()
def get_sub_parent_category(pk):
    special_offers_parent_cate = SpecialoffersSubParentCategory.objects.values('id','special_offers_sub_parent_category_name','special_offers_parent_category_id','desc').filter(special_offers_parent_category_id=pk,status='active')
    return  special_offers_parent_cate

#Special Offers Sub Parent under Parent category
@register.simple_tag()
def get_type_name(name):
    sp = SpecialoffersUnderCategory.objects.values('id',
                                                   'special_offers_parent_category_id',
                                                   'special_offers_parent_category_id__special_offers_parent_category_name',
                                                   'special_offers_parent_category_id__desc',
                                                   'special_offers_sub_parent_category_id',
                                                   'special_offers_sub_parent_category_id__special_offers_sub_parent_category_name',
                                                   'special_offers_sub_parent_category_id__desc',
                                                   'special_offers_combo_name',
                                                   'special_offers_type_name',
                                                   'province_id',
                                                   'province_id__province_name',
                                                   'city_id',
                                                   'city_id__city_name',
                                                   'telecom_name',
                                                   'telecom_logo',
                                                   'status',
                                                   ).filter(special_offers_combo_name=name,status='active')
    return sp

@register.simple_tag()
def get_sp(id,p_id):
    sp = SpecialoffersUnderCategory.objects.values('id',
                                                   'special_offers_parent_category_id',
                                                   'special_offers_parent_category_id__special_offers_parent_category_name',
                                                   'special_offers_parent_category_id__desc',
                                                   'special_offers_sub_parent_category_id',
                                                   'special_offers_sub_parent_category_id__special_offers_sub_parent_category_name',
                                                   'special_offers_sub_parent_category_id__desc',
                                                   'special_offers_combo_name',
                                                   'special_offers_type_name',
                                                   'province_id',
                                                   'province_id__province_name',
                                                   'city_id',
                                                   'city_id__city_name',
                                                   'telecom_name',
                                                   'telecom_logo',
                                                   'status',
                                                   ).filter(special_offers_sub_parent_category_id=id,status='active',
                                                            special_offers_parent_category_id=p_id).distinct('special_offers_combo_name')
    
    return sp

@register.simple_tag()
def get_hardwares_details_according_to_special_offers_plan(pk):
    sp = SpecialOffersPlanswithHardwareRates.objects.values('id','special_offers_id','hw_id','hw_id__hw_title','hw_qty','device_buy','device_rental','montly_rent','offer_price').filter(special_offers_id=pk)
    return sp


@register.simple_tag()
def get_session_province_list():
    country = 'Canada'
    
    province_data = Province.objects.values('id', 'province_name').filter(country_id__country_name=country)
    
    return  province_data


@register.simple_tag()
def get_logo():
    
    province_data = WebLogo.objects.values('id', 'image')
    
    return province_data[0]['image']