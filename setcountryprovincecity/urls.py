from django.conf.urls import url
from . import views as  setcountryprovincecity_views
urlpatterns = [

url(r'^get_country/$', setcountryprovincecity_views.get_country, name='get_country'),
url(r'^add_country/$', setcountryprovincecity_views.add_country, name='add_country'),
url(r'^edit_country/(?P<pk>[0-9]+)$', setcountryprovincecity_views.edit_country, name='edit_country'),
url(r'^delete_country/(?P<pk>[0-9]+)$', setcountryprovincecity_views.delete_country, name='delete_country'),



url(r'^get_province/$', setcountryprovincecity_views.get_province, name='get_province'),
url(r'^add_province/$', setcountryprovincecity_views.add_province, name='add_province'),
url(r'^edit_province/(?P<pk>[0-9]+)$', setcountryprovincecity_views.edit_province, name='edit_province'),
url(r'^delete_province/(?P<pk>[0-9]+)$', setcountryprovincecity_views.delete_province, name='delete_province'),


url(r'^get_city/(?P<pk>[0-9]+)$', setcountryprovincecity_views.get_city, name='get_city'),
url(r'^add_city/(?P<pk>[0-9]+)$', setcountryprovincecity_views.add_city, name='add_city'),
url(r'^edit_city/(?P<pk>[0-9]+)$', setcountryprovincecity_views.edit_city, name='edit_city'),
url(r'^delete_city/(?P<pk>[0-9]+)$', setcountryprovincecity_views.delete_city, name='delete_city'),





]