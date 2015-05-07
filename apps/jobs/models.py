# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User

from django_countries.fields import CountryField

class Jobs(models.Model):

	idjob = models.AutoField(primary_key=True)
	iduser = models.ForeignKey(User, db_index=True)
	title = models.CharField(max_length=250, null=False, blank=False)
	description = models.TextField(null=False, blank=False)
	company = models.CharField(max_length=250, null=True, blank=True)
	country = CountryField(null=False, blank=False)
	labels = models.CharField(max_length=250, null=False, blank=False)
	email = models.EmailField(null=False, blank=False)
	date = models.DateTimeField(null=False, blank=False)
