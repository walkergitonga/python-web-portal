from django.conf.urls import url

from apps.baseapp.views import (IndexView, LoginView, 
								signout, SignupView,
								ResetPassView)

urlpatterns = [
    # Examples:
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', signout, name='logout'),
    url(r'^join/$', SignupView.as_view(), name='join'),
    url(r'^reset_password/$', ResetPassView.as_view(), name='reset_password'),
]
