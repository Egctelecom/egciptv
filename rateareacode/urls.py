from django.conf.urls import url, include
from rateareacode.views import views as rateareacode_views,test
urlpatterns = [

url(r'^area_rate/$', rateareacode_views.index, name='area_rate'),
url(r'^area_rate/add/$', rateareacode_views.add, name='areacode_with_rate_add'),
url(r'^area_rate/edit/(?P<id>[0-9]+)$', rateareacode_views.edit, name='areacode_with_rate_edit'),
url(r'^area_rate/delete/(?P<id>[0-9]+)$', rateareacode_views.delete, name='areacode_with_rate_delete'),
url(r'^area_rate/status_change/$', rateareacode_views.status_changes, name='areacode_with_rate_status_change'),

]