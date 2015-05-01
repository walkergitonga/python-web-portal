from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.applications.views import (ApplicationsView, ApplicationsAddView,
									ApplicationSeeView, ApplicationEditView)

urlpatterns = [
    url(r'^applications/$', 
    	login_required(ApplicationsView.as_view()), name='applications'),
    url(r'^applications/add/$', 
    	login_required(ApplicationsAddView.as_view()), name='applications_add'),
    url(r'^application/(?P<name>.+)/(?P<username>.+)/$', 
    	login_required(ApplicationSeeView.as_view()), name='applications_view'),
    url(r'^application_edit/(?P<name>.+)/(?P<username>.+)/$', 
    	login_required(ApplicationEditView.as_view()), name='application_edit'),
]
