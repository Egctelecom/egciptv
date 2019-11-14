from django.conf.urls import url, include

from adminsidecustomer.views import views as customer_views, pending_invoice, country_province_city_view, customer_plan, \
    upload_document, contract,comment

urlpatterns = [

url(r'^customer/$', customer_views.index, name='customer'),
url(r'^change_password/(?P<pk>[0-9]+)$', customer_views.change_password, name='change_password'),
url(r'^send_password_mail/(?P<pk>[0-9]+)$', customer_views.send_password_mail, name='send_password_mail'),
url(r'^send_password_sms/(?P<pk>[0-9]+)$', customer_views.send_password_sms, name='send_password_sms'),
url(r'^customer/add/$', customer_views.add, name='add_customer'),
url(r'^customer/edit/(?P<id>[0-9]+)$', customer_views.edit, name='edit_customer'),
url(r'^customer/details/(?P<id>[0-9]+)$', customer_views.details, name='customer_details'),
url(r'^customer_delete/(?P<pk>[0-9]+)$', customer_views.customer_delete, name='customer_delete'),
url(r'^customer/custom_mail/(?P<pk>[0-9]+)$', customer_views.SendCustomMail.as_view(), name='customer_custom_mail'),

#====================== optional =================================== #
url(r'^country/$', country_province_city_view.add , name='country'), #
url(r'^city/$', country_province_city_view.city_add , name='city'),  #
#=================================================================== #

url(r'^get/province/$', country_province_city_view.get_province , name='get_province'),
url(r'^get/service/province/$', country_province_city_view.get_service_province , name='get_service_province'),
url(r'^get/city/$', country_province_city_view.get_city , name='get_city'),

url(r'^get/billing/city/$', country_province_city_view.get_billing_city , name='get_billing_city'),
url(r'^get/billing/province/$', country_province_city_view.get_billing_province , name='get_billing_province'),


#-----------------------------------------cutomer service plan----------------------------------------------#
url(r'^add_customer_service_plan/(?P<id>[0-9]+)$', customer_plan.add_user_service_price, name='add_user_service_price'),
url(r'^edit_customer_service_plan/(?P<pk>[0-9]+)$', customer_plan.edit_customer_service_plan, name='edit_customer_service_plan'),
url(r'^get_service_plan/$', customer_plan.get_service_plan, name='get_service_plan'),
url(r'^changevalue/$', customer_plan.changevalue, name='changevalue'),

url(r'^save_plan_to_user/$', customer_plan.save_plan_to_user, name='save_plan_to_user'),
url(r'^delete_plan_to_user/$', customer_plan.delete_plan_to_user, name='delete_plan_to_user'),
url(r'^delete_service_plan_to_user/(?P<pk>[0-9]+)$', customer_plan.delete_service_plan_to_user, name='delete_service_plan_to_user'),

#-----------------------------------------cutomer detils upload documents----------------------------------------------#


url(r'^upload_documents/(?P<id>[0-9]+)$', upload_document.add_upload_documents, name='upload_documents'),
url(r'^delete_upload_documents/(?P<id>[0-9]+)$', upload_document.delete_upload_documents, name='delete_upload_documents'),

url(r'^create_tickets/(?P<id>[0-9]+)$', upload_document.create_tickets, name='create_tickets'),
url(r'^edit_tickets/(?P<id>[0-9]+)$', upload_document.edit_tickets, name='edit_tickets'),
url(r'^delete_tickets/(?P<id>[0-9]+)$', upload_document.delete_tickets, name='delete_tickets'),


#-----------------------------------------pending invoice details----------------------------------------------#
url(r'^add_pending_invoice_details/(?P<id>[0-9]+)$', pending_invoice.add_pending_invoice_details, name='add_pending_invoice_details'),

#-----------------------------------------Contract with service----------------------------------------------#

url(r'^create_new_contract/(?P<id>[0-9]+)$', contract.create_new_contract, name='create_new_contract'),
url(r'^terminate_contract/(?P<id>[0-9]+)$', contract.terminate_contract, name='terminate_contract'),
url(r'^renew_contract/(?P<id>[0-9]+)$', contract.renew_contract, name='renew_contract'),
url(r'^view_contract/(?P<id>[0-9]+)$', contract.view_contract, name='view_contract'),
url(r'^email_resend/(?P<id>[0-9]+)/(?P<contract_id>[0-9]+)$', contract.email_resend, name='email_resend'),
url(r'^email_contract/(?P<id>[0-9]+)$', contract.email_contract, name='email_contract'),


#-----------------------------------------Contract with service add to list hardware----------------------------------------------#

url(r'^get_hw_service_plan/$', contract.get_hw_service_plan, name='get_hw_service_plan'),

#----------------------------------------- Paypal ----------------------------------------------#

url(r'^go_for_payment/(?P<id>[0-9]+)$', contract.go_for_payment, name='go_for_payment'),

#================================ PDF ===========================================================#

url(r'^pdf/', include('pdf.urls')),

#================================ Comment ========================================================#
url(r'^comment/(?P<id>[0-9]+)$', comment.index, name='comment'),
url(r'^save_comment/$', comment.save_comment, name='save_comment'),

#================================ others =========================================================#

url(r'^get_service_with_ticket/$', upload_document.get_service_with_ticket, name='get_service_with_ticket'),
url(r'^get_service_hw_with_ticket/$', upload_document.get_service_hw_with_ticket, name='get_service_hw_with_ticket'),

#================================================================= Customer contract with mac address of each h/w for each user ================================================================

url(r'^view_hw_MAC/(?P<pk>[0-9]+)/(?P<customer_pk>[0-9]+)/(?P<id>[0-9]+)$', customer_views.view_hw_MAC, name='view_hw_MAC'),
url(r'^edit_hw_MAC/(?P<pk>[0-9]+)/(?P<customer_pk>[0-9]+)/(?P<id>[0-9]+)$', customer_views.edit_hw_MAC, name='edit_hw_MAC'),


url(r'^viewcontractfrench/$', contract.view_contract_french, name='viewcontractfrench'),

# ==================================================Set mpn========================================================#

# url(r'^set_mnp/(?P<customer_pk>[0-9]+)$',customer_views.set_mnp, name='set_mnp'),

url(r'^port_number/(?P<customer_pk>[0-9]+)$',customer_views.port_number, name='port_number'),

url(r'^set_mnp_add',customer_views.set_mnp_add, name='set_mnp_add'),
url(r'^save_port_number',customer_views.save_port_number, name='save_port_number'),

#=================================================== CDR Records ===================================================#

url(r'^cdr_number_records/(?P<number>[0-9]+)/(?P<customer_id>[0-9]+)$',customer_views.cdr_number_records, name='cdr_number_records'),

url(r'^same_as_account_address$',customer_views.same_as_account_address, name='same_as_account_address'),

#=================================================== Change Account status of Customer  ===================================================#

url(r'^change_account_status_of_customer',customer_views.change_account_status_of_customer, name='change_account_status_of_customer'),




]
