from django.conf.urls import url, include

from customer_billing.views import CustomerDetails, CustomerBillingAdd, CustomerBillingEdit

urlpatterns = [
	url(r'^billing/list/$', CustomerDetails.as_view(), name='customer_billing_details'),
	url(r'^billing/add/$', CustomerBillingAdd.as_view(), name='customer_billing_add'),
	url(r'^billing/edit/(?P<id>[0-9]+)$', CustomerBillingEdit.as_view(), name='customer_billing_edit'),
]