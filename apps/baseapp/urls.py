from django.conf.urls import url

from apps.baseapp.views import IndexView 

urlpatterns = [
    # Examples:
     url(r'^$', IndexView.as_view(), name='index'),
]
