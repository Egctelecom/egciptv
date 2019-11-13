from django.conf.urls import url
from crmadmin.views import views as admin_views

urlpatterns = [
    url(r'^$', admin_views.admin_login, name='admin_login'),
    url(r'^dashboard/$', admin_views.admin_dashboard, name='dashboard'),
    url(r'^logout/$', admin_views.admin_signout, name='signout'),
    url(r'^save_avatar/$', admin_views.save_avatar, name='save_avatar'),
    url(r'^user_info/$', admin_views.user_info, name='user_info'),

    # ================================= save profile email ======================================================================#

    url(r'^saveprofile/$', admin_views.saveprofile, name='saveprofile'),

    # ================================ Forget Password ==========================================================================#

    url(r'^send_mail_for_forget_password/$', admin_views.send_mail_for_forget_password, name='send_mail_for_forget_password'),
    url(r'^checkotp/$', admin_views.checkotp, name='checkotp'),
    url(r'^paswordchange/$', admin_views.paswordchange, name='paswordchange'),

   ]