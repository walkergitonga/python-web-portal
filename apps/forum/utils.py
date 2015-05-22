# -*- coding: UTF-8 -*-
import os

from django.conf import settings
from django.shortcuts import get_object_or_404

from apps.forum.models import Forum, Topic
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
