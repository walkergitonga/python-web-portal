# -*- coding: UTF-8 -*-
import os

from django.db.models import get_model
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.utils import formats, timezone
from django.utils.translation import ugettext_lazy as _

from apps.forum.models import (
	Forum, Topic, Comment, Notification
)
from apps.forum.settings import (
	APP_PROFILE, MODEL_PROFILE,
	URL_PROFILE, FIELD_PHOTO_PROFILE
)
from apps.utils import (
	remove_folder, exists_folder
)


def get_folder_attachment(topic):
	'''
		This method return the path of one
		folder attachment for app forum
	'''
	folder = ""
	folder = "forum_" + str(topic.forum_id)
	folder = folder + "_user_" + str(topic.user.username)
	folder = folder + "_topic_" + str(topic.id_attachment)
	path_folder = os.path.join("forum", folder)
	media_path = settings.MEDIA_ROOT
	path = media_path + "/" +  path_folder

	return path


def remove_folder_attachment(idtopic):
	'''
		This method remove folder attachment
		and subtract one topic.
	'''
	# Subtract one topic
	topic = get_object_or_404(Topic, idtopic=idtopic)
	forum = get_object_or_404(Forum, name=topic.forum, hidden=False)
	tot = forum.topics_count
	tot = tot - 1
	Forum.objects.filter(name=topic.forum, hidden=False).update(
		topics_count=tot
	)

	path = get_folder_attachment(topic)

	# Remove attachment if exists
	if exists_folder(path):
		remove_folder(path)


def get_id_profile(iduser):
	'''
		This method return one id
		of model profile
	'''
	Profile = get_model(APP_PROFILE, MODEL_PROFILE)
	profile = get_object_or_404(Profile, iduser_id=iduser)

	return profile


def get_photo_profile(profile):

	'''
		This method return the photo
		of model profile id
	'''
	field_photo = getattr(profile, FIELD_PHOTO_PROFILE)
	return field_photo


def get_users_topic(topic, myuser):
	'''
		This method return all users
		of one topic, else my user
	'''
	comments = Comment.objects.filter(topic_id=topic.idtopic)
	lista_us = []
	for comment in comments:
		if comment.user_id != myuser:
			if not comment.user_id in lista_us:
				lista_us.append(comment.user_id)

	return lista_us


def get_notifications(iduser):
	'''
		This method return Notification
		of one user
	'''
	try:
		notif = Notification.objects.filter(
					iduser=iduser).order_by("-date")
	except Notification.DoesNotExist:
		notif = None

	return notif


def get_datetime_topic(date):
	'''
		This method return info
		one datetime for topic or
		notification
	'''
	flag = True
	now = timezone.now()
	# If is beteween 1 and 10 return days
	difference = (now - date).days

	# If is this days return hours
	if difference == 0:
		flag = False
		diff = now - date
		minutes = (diff.seconds//60)%60
		hours = diff.seconds//3600
		if minutes < 60 and hours == 0:
			difference =  "%s %s" % (str((diff.seconds//60)%60) + "m ", _("ago"))
		else:
			difference =  "%s %s" % (str(diff.seconds//3600) + "h ", _("ago"))

	# If > 10 days return string date
	if difference > 1 and difference <= 10:
		flag = False
		difference = formats.date_format(date, "SHORT_DATETIME_FORMAT")

	if flag:
		difference = "%s %s" % (str(difference),  _("days ago"))

	return difference
