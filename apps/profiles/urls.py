from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.profiles.views import EditProfileView, ProfileView

urlpatterns = [
    url(r'^profile/$', 
    	login_required(ProfileView.as_view()), name='profile'),
    url(r'^edit_profile/$', 
    	login_required(EditProfileView.as_view()), name='edit_profile'),
]
