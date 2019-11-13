from django.conf.urls import url
from . import views as number_views

urlpatterns = [

url(r'^number/$', number_views.index, name='number'),

]