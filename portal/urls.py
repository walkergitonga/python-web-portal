from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    url(r'^' , include('apps.baseapp.urls')),
    url(r'^' , include('apps.profiles.urls')),
    url(r'^' , include('apps.applications.urls')),
    url(r'^' , include('apps.jobs.urls')),
    url(r'^' , include('apps.forum.urls')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^admin/', include(admin.site.urls)),
] 

if settings.DEBUG:
	from django.conf.urls.static import static
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
