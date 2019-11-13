from crmadmin.urlsuserloginswithsettings import urlpatterns as urlsuserloginswithsettings
from crmadmin.urlswithadmin import urlpatterns as urlswithadmin
from crmadmin.urlswithsettings import urlpatterns as urlswithsettings
from crmadmin.urlsmanageservicewithsettings import urlpatterns as urlsmanageservicewithsettings
from crmadmin.urls_service import urlpatterns as urls_service
from adminsidecustomer.urls import urlpatterns as urls_adminsidecustomer
from adminsideserviceprovider.urls import urlpatterns as urls_adminsideserviceprovider
from adminnumberprovider.urls import urlpatterns as urls_adminnumberprovider
from crmadmin.url_agent import urlpatterns as url_agent
from crmadmin.urls_agent_permission import urlpatterns as urls_agent_permission
from crmadmin.urls_ticket import urlpatterns as urls_ticket
from crmadmin.url_cdr import urlpatterns as urls_cdr
from crmadmin.urls_tax import urlpatterns as urls_tax
from rateareacode.urls import urlpatterns as area_ulrs
from ratecustomerbillingwithcdr.urls import urlpatterns as billing_ulrs
from setcountryprovincecity.urls import urlpatterns as setcountryprovincecity_ulrs
from settingcontractsheet.urls import urlpatterns as settingcontractsheet_urls
from sitefrontendbyadmin.urls import urlpatterns as sitefrontendbyadmin_urls
from crmadmin.applied_users_urls import urlpatterns as applied_users_urls
from crmadmin.url_special_offer import urlpatterns as url_special_offer
from crmadmin.urls_other_details import urlpatterns as urls_other_details


urlpatterns = urlswithadmin
urlpatterns += urlswithsettings
urlpatterns += urlsmanageservicewithsettings
urlpatterns += urlsuserloginswithsettings
urlpatterns += urls_service
urlpatterns += urls_adminsidecustomer
urlpatterns += urls_adminsideserviceprovider
urlpatterns += urls_adminnumberprovider
urlpatterns += url_agent
urlpatterns += urls_agent_permission
urlpatterns += urls_ticket
urlpatterns += urls_cdr
urlpatterns += urls_tax
urlpatterns += area_ulrs
urlpatterns += billing_ulrs
urlpatterns += setcountryprovincecity_ulrs
urlpatterns += settingcontractsheet_urls
urlpatterns += sitefrontendbyadmin_urls
urlpatterns += applied_users_urls
urlpatterns += url_special_offer
urlpatterns += urls_other_details
