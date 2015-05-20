# -*- coding: UTF-8 -*-
import os

from django.conf import settings

def get_folder_attachment(topic):
	'''
		This method return the path
		of one folder attachment
	'''
	folder = ""
	folder = "forum_" + str(topic.forum_id) 
	folder = folder + "_user_" + str(topic.user.username) 
	folder = folder + "_topic_" + str(topic.id_attachment)
	path_folder = os.path.join("forum", folder)
	media_path = settings.MEDIA_ROOT
	path = media_path + "/" +  path_folder

	return path