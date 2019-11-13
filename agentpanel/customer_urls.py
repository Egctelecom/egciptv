from django.conf.urls import url, include

from agentpanel.views import customer_views as customer_views
from agentpanel.views import pending_invoice as pending_invoice
from agentpanel.views import country_province_city_view as country_province_city_view
from agentpanel.views import customer_plan as customer_plan
from agentpanel.views import upload_document as upload_document
from agentpanel.views import contract as contract

urlpatterns = [

url(r'^customer/$', customer_views.index, name='agent_customer'),
url(r'^customer/add/$', customer_views.add, name='agent_add_customer'),
url(r'^customer/edit/(?P<id>[0-9]+)$', customer_views.edit, name='agent_edit_customer'),
url(r'^customer/details/(?P<id>[0-9]+)$', customer_views.details, name='agent_customer_details'),

#====================== optional =================================== #
url(r'^country/$', country_province_city_view.add , name='agent_country'), #
url(r'^city/$', country_province_city_view.city_add , name='agent_city'),  #
#=================================================================== #

url(r'^get/province/$', country_province_city_view.get_province , name='agent_get_province'),
url(r'^get/city/$', country_province_city_view.get_city , name='agent_get_city'),

url(r'^get/billing/city/$', country_province_city_view.get_billing_city , name='agent_get_billing_city'),
url(r'^get/billing/province/$', country_province_city_view.get_billing_province , name='agent_get_billing_province'),


#-----------------------------------------cutomer service plan----------------------------------------------#
url(r'^add_customer_service_plan/(?P<id>[0-9]+)$', customer_plan.add_user_service_price, name='agent_add_user_service_price'),
url(r'^get_service_plan/$', customer_plan.get_service_plan, name='agent_get_service_plan'),
url(r'^changevalue/$', customer_plan.changevalue, name='agent_changevalue'),

url(r'^save_plan_to_user/$', customer_plan.save_plan_to_user, name='agent_save_plan_to_user'),
url(r'^delete_plan_to_user/$', customer_plan.delete_plan_to_user, name='agent_delete_plan_to_user'),

#-----------------------------------------cutomer detils upload documents----------------------------------------------#


url(r'^upload_documents/(?P<id>[0-9]+)$', upload_document.add_upload_documents, name='agent_upload_documents'),
url(r'^delete_upload_documents/(?P<id>[0-9]+)$', upload_document.delete_upload_documents, name='agent_delete_upload_documents'),

url(r'^create_tickets/(?P<id>[0-9]+)$', upload_document.create_tickets, name='agent_create_tickets'),
url(r'^edit_tickets/(?P<id>[0-9]+)$', upload_document.edit_tickets, name='agent_edit_tickets'),
url(r'^delete_tickets/(?P<id>[0-9]+)$', upload_document.delete_tickets, name='agent_delete_tickets'),


#-----------------------------------------pending invoice details----------------------------------------------#
url(r'^add_pending_invoice_details/(?P<id>[0-9]+)$', pending_invoice.add_pending_invoice_details, name='agent_add_pending_invoice_details'),

#-----------------------------------------Contract with service----------------------------------------------#

url(r'^create_new_contract/(?P<id>[0-9]+)$', contract.create_new_contract, name='agent_create_new_contract'),
url(r'^terminate_contract/(?P<id>[0-9]+)$', contract.terminate_contract, name='agent_terminate_contract'),
url(r'^renew_contract/(?P<id>[0-9]+)$', contract.renew_contract, name='agent_renew_contract'),
url(r'^view_contract/(?P<id>[0-9]+)$', contract.view_contract, name='agent_view_contract'),
url(r'^email_resend/(?P<id>[0-9]+)/(?P<contract_id>[0-9]+)$', contract.email_resend, name='agent_email_resend'),
url(r'^email_contract/(?P<id>[0-9]+)$', contract.email_contract, name='agent_email_contract'),


#-----------------------------------------Contract with service add to list hardware----------------------------------------------#

url(r'^get_hw_service_plan/$', contract.get_hw_service_plan, name='agent_get_hw_service_plan'),

#----------------------------------------- Paypal ----------------------------------------------#

url(r'^go_for_payment/(?P<id>[0-9]+)$', contract.go_for_payment, name='agent_go_for_payment'),

#================================ PDF ===========================================================#

url(r'^pdf/', include('pdf.urls')),

]
