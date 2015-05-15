from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.forum.views import (
	ForumsView, ForumView,
	TopicView, NewTopicView
)

urlpatterns = [
	url(
		r'^forums/$', ForumsView.as_view(), name='forums'
	),
	url(
		r'^forum/(?P<forum>.+)/$', ForumView.as_view(), name='forum'
	),
	url(
		r'^topic/(?P<forum>.+)/(?P<slug>[-\w]+)/(?P<idtopic>\d+)/$', TopicView.as_view(), name='topic'
	),
	url(
		r'^newtopic/(?P<forum>.+)/$', login_required(NewTopicView.as_view()), name='newtopic'
	),
]
