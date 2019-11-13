from django import template
from egciptvhome.models import Otherdetails
from django.http import HttpResponse
from adminsideserviceprovider.models import ManageServicePricedoc,ServicePlanWithHardware
from sitefrontendbyadmin.models import Specialoffersdoc
from ratecustomerbillingwithcdr.models import VoipLongDistanceRate
import re

register = template.Library()


@register.simple_tag()
def other_section_data(cname):
	other_details = Otherdetails.objects.values('id', 'key', 'value').filter(key=cname)
	return other_details


@register.simple_tag()
def get_plans_doc(pk):
	other_details = ManageServicePricedoc.objects.values('id', 'service_price_doc_name','status','service_price_doc').filter(service_price_provider_id=pk)
	return other_details


@register.simple_tag()
def get_special_offers_doc(pk):
	other_details = Specialoffersdoc.objects.values('id', 'special_offers_doc_name','status','special_offers_doc').filter(special_offers_id=pk)
	return other_details


@register.simple_tag()
def get_voip_distence(tx):
	text = tx
	text = re.escape(text)  # make sure there are not regex specials
	data = VoipLongDistanceRate.objects.values('id', 'country', 'prefix', 'rate').filter(
		country__iregex=r"(^|\s)%s" % text)
	return data


@register.simple_tag()
def get_service_provider_hw(id):
		sp = ServicePlanWithHardware.objects.values('hw_id','hw_id__hw_title','hw_qty','hw_id__device_buy').filter(service_plan_id=id)
		return sp


	
	
	
