from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.forum.views import ForumsView, ForumView

urlpatterns = [
	url(
		r'^forums/$', ForumsView.as_view(), name='forums'
	),
	url(
		r'^forum/(?P<forum>.+)/$', ForumView.as_view(), name='forum'
	),
]
