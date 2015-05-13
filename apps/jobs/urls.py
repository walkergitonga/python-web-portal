from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.jobs.views import (
    JobsView, JobsAddView, JobSeeView,
    JobDeleteView, JobEditView
)

urlpatterns = [
    url(
        r'^jobs/$', JobsView.as_view(), name='jobs'
    ),
    url(
        r'^jobs/add/$', login_required(JobsAddView.as_view()), 
        name='jobs_add'
    ),
    url(
        r'^job/(?P<idjob>\d+)/(?P<username>.+)/$', JobSeeView.as_view(), 
        name='job_view'
    ),
    url(
        r'^job_delete/(?P<idjob>\d+)/(?P<username>.+)/$', 
        login_required(JobDeleteView.as_view()), name='Job_delete'
    ),
    url(
        r'^job_edit/(?P<idjob>\d+)/(?P<username>.+)/$', 
        login_required(JobEditView.as_view()), name='job_edit'
    ),
]
