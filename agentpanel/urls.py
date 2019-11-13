from agentpanel.urlswithadmin import urlpatterns as urlswithadmin
from agentpanel.service_provider_urls import urlpatterns as service_provider_urls
from agentpanel.urlswithsettings import urlpatterns as urlswithsettings
from agentpanel.urls_service import urlpatterns as urls_service
from agentpanel.customer_urls import urlpatterns as customer_urls
from agentpanel.number_urls import urlpatterns as number_urls
from agentpanel.urlsmanageservicewithsettings import urlpatterns as urlsmanageservicewithsettings
from agentpanel.urlsuserloginswithsettings import urlpatterns as urlsuserloginswithsettings



urlpatterns = urlswithadmin
urlpatterns += service_provider_urls
urlpatterns += urlswithsettings
urlpatterns += urls_service
urlpatterns += customer_urls
urlpatterns += number_urls
urlpatterns += urlsmanageservicewithsettings
urlpatterns += urlsuserloginswithsettings

