from django.conf.urls import url
from . import views as paypal_views
urlpatterns = [

url(r'^$', paypal_views.paypalIPN, name='paypal'),
url(r'^paypal/complete/$', paypal_views.paypalIPN, name='paypal_complete'),

]