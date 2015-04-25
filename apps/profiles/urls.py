from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from apps.profiles.views import (EditProfileView, ProfileView,
								AdminView)

urlpatterns = [
    url(r'^profile/$', 
    	login_required(ProfileView.as_view()), name='profile'),
    url(r'^settings/edit_profile/$', 
    	login_required(EditProfileView.as_view()), name='edit_profile'),
    url(r'^settings/admin/$', 
    	login_required(AdminView.as_view()), name='admin_password'),
]
