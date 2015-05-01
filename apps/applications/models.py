# -*- coding: UTF-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Applications(models.Model):

	idapp = models.AutoField(primary_key=True)
	iduser = models.ForeignKey(User, db_index=True)
	name = models.CharField(max_length=250, unique=True, null=False, blank=False)
	description = models.TextField(null=False, blank=False)
	repository = models.CharField(max_length=250, null=False, blank=False)