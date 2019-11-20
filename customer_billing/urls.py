from django.conf.urls import url, include

from customer_billing.views import CustomerDetails, CustomerBillingAdd, CustomerBillingEdit, CreditCardListView, \
	CreditCardAdd

urlpatterns = [
	url(r'^billing/list/$', CustomerDetails.as_view(), name='customer_billing_details'),
	url(r'^billing/add/$', CustomerBillingAdd.as_view(), name='customer_billing_add'),
	url(r'^billing/edit/(?P<id>[0-9]+)$', CustomerBillingEdit.as_view(), name='customer_billing_edit'),
	
	# Credit Card
	url(r'^creditcard/list/(?P<id>[0-9]+)$', CreditCardListView.as_view(), name='customer_credit_card'),
	url(r'^creditcard/(?P<id>[0-9]+)/add$', CreditCardAdd.as_view(), name='customer_credit_card_add'),
	
]
