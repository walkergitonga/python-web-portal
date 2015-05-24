# encoding:utf-8
from django import template
from django.db.models import get_model
from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.shortcuts import get_object_or_404

from apps.forum.settings import (
	APP_PROFILE, MODEL_PROFILE,
	FIELD_PHOTO_PROFILE
)

register = template.Library()


@register.filter
def get_photo(user):
	'''
	This tag return the path photo profile
	'''
	Profile = get_model(APP_PROFILE, MODEL_PROFILE)

	profile = get_object_or_404(Profile, iduser_id=user)
	field_photo = getattr(profile, FIELD_PHOTO_PROFILE)

	if not field_photo:
		field_photo = static("img/profile.png")
	else:
		field_photo = settings.MEDIA_URL + str(field_photo)

	return field_photo
