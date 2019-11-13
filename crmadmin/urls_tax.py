from django.conf.urls import url
from crmadmin.views import sales_tax as  sales_tax_views
urlpatterns = [

url(r'^sales_tax/$', sales_tax_views.sales_tax_details, name='sales_tax'),
url(r'^add_sales_tax/$', sales_tax_views.add_sales_tax, name='add_sales_tax'),
url(r'^edit_sales_tax/(?P<pk>[0-9]+)$', sales_tax_views.edit_sales_tax, name='edit_sales_tax'),
url(r'^delete_sales_tax/(?P<pk>[0-9]+)$', sales_tax_views.delete_sales_tax, name='delete_sales_tax'),

]