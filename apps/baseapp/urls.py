from django.conf.urls import url

from apps.baseapp.views import IndexView, LoginView, signout

urlpatterns = [
    # Examples:
     url(r'^$', IndexView.as_view(), name='index'),
     url(r'^login/$', LoginView.as_view(), name='login'),
     url(r'^logout/$', signout, name='logout'),
]
