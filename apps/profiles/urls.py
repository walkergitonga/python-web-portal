from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.profiles.views import ProfileView

urlpatterns = [
    url(r'^profile/$', 
    	login_required(ProfileView.as_view()), name='profile'),
]
