from django.conf.urls import url, include

from customer_billing.views import CustomerDetails, CustomerBillingAdd, CustomerBillingEdit, CreditCardListView, \
	CreditCardAdd, CreditCardEditView, CreditCardImport, DirectDeopsitAdd, PaypalAddressAdd, DirectDeopsitEdit, PaypalAddressEdit, \
	CreditCardEditDelete, DirectDeopsitDelete, PaypalAddressDelete, CustomerBillingSetting

urlpatterns = [
	url(r'^billing/list/$', CustomerDetails.as_view(), name='customer_billing_details'),
	url(r'^billing/add/$', CustomerBillingAdd.as_view(), name='customer_billing_add'),
	url(r'^billing/setting/$', CustomerBillingSetting.as_view(), name='customer_billing_setting'),
	url(r'^billing/edit/(?P<id>[0-9]+)$', CustomerBillingEdit.as_view(), name='customer_billing_edit'),
	
	# Credit Card
	url(r'^creditcard/list/(?P<id>[0-9]+)$', CreditCardListView.as_view(), name='customer_credit_card'),
	url(r'^creditcard/(?P<id>[0-9]+)/add$', CreditCardAdd.as_view(), name='customer_credit_card_add'),
	url(r'^creditcard/edit/(?P<id>[0-9]+)$', CreditCardEditView.as_view(), name='customer_credit_card_edit'),
	url(r'^creditcard/delete/(?P<id>[0-9]+)$', CreditCardEditDelete.as_view(), name='customer_credit_card_delete'),
	url(r'^creditcard/(?P<id>[0-9]+)/import', CreditCardImport.as_view(), name='customer_credit_card_import'),
	
	#Direct Deposit
	url(r'^directdeposit/(?P<id>[0-9]+)/add', DirectDeopsitAdd.as_view(), name='customer_direct_deposit_add'),
	url(r'^directdeposit/(?P<id>[0-9]+)/edit', DirectDeopsitEdit.as_view(), name='customer_direct_deposit_edit'),
	url(r'^directdeposit/(?P<id>[0-9]+)/delete', DirectDeopsitDelete.as_view(), name='customer_direct_deposit_delete'),
	
	
	#Paypal address
	url(r'^paypaladdress/(?P<id>[0-9]+)/add', PaypalAddressAdd.as_view(), name='customer_paypal_address_add'),
	url(r'^paypaladdress/(?P<id>[0-9]+)/edit', PaypalAddressEdit.as_view(), name='customer_paypal_address_edit'),
	url(r'^paypaladdress/(?P<id>[0-9]+)/delete', PaypalAddressDelete.as_view(), name='customer_paypal_address_delete'),
]
