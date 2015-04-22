from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class Profile(models.Model):

	idprofile = models.AutoField(primary_key=True)
	iduser = models.ForeignKey(User, db_index=True)
	photo = models.FileField(upload_to=settings.MEDIA_URL + "profiles/", null=True)
	location = models.CharField(max_length=200, null=True)
	company = models.CharField(max_length=150, null=True)