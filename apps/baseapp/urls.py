from django.conf.urls import url

from apps.baseapp.views import (IndexView, LoginView, 
								signout, SignupView,
								reset_password, pass_reset_done,
								reset_pass_confirm, reset_done_pass)

urlpatterns = [
    # Examples:
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', signout, name='logout'),
    url(r'^join/$', SignupView.as_view(), name='join'),
    url(r'^reset_password/$', reset_password, name='password_reset'),
	url(r'^reset_password/done/$', pass_reset_done, name='password_reset_done'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 
		reset_pass_confirm, name='password_reset_confirm'),
	url(r'^reset/done/$', reset_done_pass, name='password_reset_complete'),

]
