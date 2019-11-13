from random import randint

from django import template

from sitefrontendbyadmin.models import SpecialOffersPlans,SpecialoffersParentCategory,SpecialoffersSubParentCategory,SpecialoffersUnderCategory

register = template.Library()



# Get Special Offers Parent Category

@register.simple_tag()
def getOffersParentCategory():
    servies_offers = SpecialoffersParentCategory.objects.values('id',
                                                                'special_offers_parent_category_name',
                                                                'desc',
		                                                        'status'
                                                                ).filter(status='active')
    return servies_offers


# Get Special Offers  Sub Parent Category

@register.simple_tag()
def getOffersSubParentCategory(pk):
    servies_offers = SpecialoffersSubParentCategory.objects.values('id',
                                                                   'special_offers_sub_parent_category_name',
                                                                   'desc',
		                                                           'status').filter(special_offers_parent_category_id=pk,status='active')
    return servies_offers

# Get Special Offers Plan

@register.simple_tag()
def getOffersPlans(pk):
    servies_offers = SpecialOffersPlans.objects.values('id', 'service_price_id__service_name').filter(special_offers_id=pk)
    return servies_offers


@register.simple_tag()
def spcial_offers_type(pk):
    
    i=0
    if SpecialoffersUnderCategory.objects.filter(special_offers_sub_parent_category_id=pk).exists():
        i = i+1
        
    return i
    
@register.simple_tag()
def getspecialoffersidlist(id,arry):
    i=0
    for ar in arry:
        if id == ar:
            i = i+1
            return i
        
        
@register.simple_tag()
def get_type_read_name(parent_id,sub_parent_id,combo_name):
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
                                                   ).filter(special_offers_parent_category_id=parent_id,
                                                            special_offers_sub_parent_category_id=sub_parent_id,
                                                            special_offers_combo_name=combo_name)
    
    return sp
    
    


