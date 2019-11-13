from django.conf.urls import url
from agentpanel.views import views as agent_views

urlpatterns = [
    url(r'^$', agent_views.agent_login, name='agent_login'),
    url(r'^dashboard/$', agent_views.agent_dashboard, name='agent_dashboard'),
    url(r'^logout/$', agent_views.agent_signout, name='agent_signout'),

    # ================================= save profile email ======================================================================#

    url(r'^saveprofile/$', agent_views.saveprofile, name='agent_saveprofile'),

    # ================================ Forget Password ==========================================================================#

    url(r'^send_mail_for_forget_password/$', agent_views.send_mail_for_forget_password, name='agent_send_mail_for_forget_password'),
    url(r'^checkotp/$', agent_views.checkotp, name='agent_checkotp'),
    url(r'^paswordchange/$', agent_views.paswordchange, name='agent_paswordchange'),
   ]