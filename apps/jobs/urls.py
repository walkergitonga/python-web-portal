from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.jobs.views import JobsView, JobsAddView

urlpatterns = [
    url(r'^jobs/$', 
    	JobsView.as_view(), name='jobs'),
    url(r'^jobs/add/$', 
        login_required(JobsAddView.as_view()), name='jobs_add'),
]
