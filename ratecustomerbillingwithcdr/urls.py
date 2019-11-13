from django.conf.urls import url, include
from ratecustomerbillingwithcdr.views import views as ratecustomerbillingwithcdr_views,voip_long_distance_rate_views
urlpatterns = [

url(r'^rate_customer_billing_cdr/(?P<id>[0-9]+)$', ratecustomerbillingwithcdr_views.index, name='rate_customer_billing_cdr'),
url(r'^rate_customer_billing_cdr_test/$', ratecustomerbillingwithcdr_views.test, name='rate_customer_billing_cdr_test'),
url(r'^rate_customer_billing_cdr_billing_details/(?P<id>[0-9]+)$', ratecustomerbillingwithcdr_views.billing_details, name='rate_customer_billing_cdr_billing_details'),
url(r'^rate_customer_billing_cdr_billing_details_edited/(?P<id>[0-9]+)$', ratecustomerbillingwithcdr_views.billing_details_edited, name='rate_customer_billing_cdr_billing_details_edited'),
url(r'^rate_customer_billing_cdr_billing_edit/(?P<id>[0-9]+)$', ratecustomerbillingwithcdr_views.billing_edit, name='rate_customer_billing_cdr_billing_edit'),
url(r'^rate_customer_billing_cdr_billing_edit_data/(?P<id>[0-9]+)$', ratecustomerbillingwithcdr_views.rate_customer_billing_cdr_billing_edit_data, name='rate_customer_billing_cdr_billing_edit_data'),


# Voip Long Distance Rate

url(r'^voip_distance_rate/excel/import/$', voip_long_distance_rate_views.voip_distance_rate_excel_import, name='voip_distance_rate_excel_import'),
url(r'^voip_distance_rate/view/$', voip_long_distance_rate_views.voip_distance_rate_view, name='voip_distance_rate_view'),




]