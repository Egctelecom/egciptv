from django.conf.urls import url
from . import views as  settingcontractsheet_views
urlpatterns = [

  url(r'^update_contract_sheet/(?P<pk>[0-9]+)$', settingcontractsheet_views.update_contract_sheet, name='update_contract_sheet'),
  url(r'^save_contractsheet/$', settingcontractsheet_views.save_contractsheet, name='save_contractsheet'),


]