from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.applications.views import (ApplicationsView, ApplicationsAddView,
									ApplicationSeeView)

urlpatterns = [
    url(r'^applications/$', 
    	login_required(ApplicationsView.as_view()), name='applications'),
    url(r'^applications/add/$', 
    	login_required(ApplicationsAddView.as_view()), name='applications_add'),
    url(r'^application/(?P<name>.+)/(?P<username>.+)/$', 
    	login_required(ApplicationSeeView.as_view()), name='applications_view'),
]
