from django.conf.urls import url
from crmadmin.views import apply_users as  apply_users_views
urlpatterns = [

   url(r'^apply_user/$', apply_users_views.apply_user, name='apply_user'),
   url(r'^apply/user/profile/(?P<pk>[0-9]+)$', apply_users_views.apply_user_profile, name='apply_user_profile'),
   url(r'^send_mail/apply_user/$', apply_users_views.send_mail_to_apply_user, name='send_mail_to_apply_user'),
   url(r'^apply_user/activated/$', apply_users_views.set_to_activated_users, name='set_to_activated_users'),
   url(r'^apply_user/user/activated/$', apply_users_views.set_to_user, name='set_to_user'),
	
]