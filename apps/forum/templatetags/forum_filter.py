# encoding:utf-8
from django import template

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.text import Truncator

from hitcount.models import HitCount

from apps.forum.models import (
	Comment, Forum, Topic,
	Notification
)
from apps.forum.templatetags.photo import get_photo
from apps.forum.utils import get_id_profile, get_photo_profile

register = template.Library()


@register.filter
def in_category(category):
	'''
	This tag filter the forum for category
	'''
	return Forum.objects.filter(
		category_id=category,
		hidden=False
	)


@register.filter
def get_tot_comments(idtopic):
	'''
	This tag filter return the total
	comments of one topic
	'''
	return Comment.objects.filter(
		topic_id=idtopic,
	).count()


@register.simple_tag
def get_tot_views(idtopic):
	'''
	This tag filter return the total
	views for topic or forum
	'''
	try:
		content = Topic.objects.get(idtopic=idtopic)
		idobj = ContentType.objects.get_for_model(content)

		hit = HitCount.objects.get(
			object_pk=idtopic,
			content_type_id=idobj
		)
		total = hit.hits
	except Exception:
		total = 0

	return total


@register.filter
def get_tot_users_comments(topic):
	'''
	This tag filter return the total
	users of one topic
	'''
	idtopic = topic.idtopic
	users = Comment.objects.filter(topic_id=idtopic)

	data = ""
	lista = []
	for user in users:
		usuario = user.user.username
		if not usuario in lista:
			lista.append(usuario)

			photo = get_photo(user.user.id)

			tooltip = ""
			tooltip += "data-toggle='tooltip' data-placement='bottom'"
			tooltip += "title='"+ usuario +"'"
			data += "<a href='/profile/"+ usuario +"' "+tooltip+" >"
			data += "<img class='img-circle' src='"+str(photo)+"' "
			data += "width=30, height=30></a>"

	if len(users) == 0:
		usuario = topic.user.username
		iduser = topic.user.id

		photo = get_photo(iduser)
		tooltip = ""
		tooltip += "data-toggle='tooltip' data-placement='bottom'"
		tooltip += "title='"+ usuario +"'"
		data += "<a href='/profile/"+ usuario +"' "+tooltip+" >"
		data += "<img class='img-circle' src='"+str(photo)+"' "
		data += "width=30, height=30></a>"


	return data


@register.filter
def get_tot_topics_moderate(forum):
	'''
		This filter return info about
		Few topics missing for moderate
	'''
	topics_count = forum.topics_count
	idforum = forum.idforum

	moderates = Topic.objects.filter(
							forum_id=idforum,
							moderate=True).count()
	return topics_count - moderates


@register.filter
def get_item_notification(notification):
	'''
		This filter return info about
		one notification of one user
	'''
	idobject = notification.idobject
	is_comment = notification.is_comment
	is_topic = notification.is_comment

	html = ""
	if is_comment:
		try:
			comment = Comment.objects.get(idcomment=idobject)

			forum = comment.topic.forum.name
			slug = comment.topic.slug
			idtopic = comment.topic.idtopic

			description = Truncator(comment.description).chars(100)

			url_topic = "/topic/" + forum + "/" + slug + "/" + str(idtopic) + "/"
 			html += "<h5><a href='"+url_topic+"'><u>"+comment.topic.title+"</u></h5></a>"
			html += "<p>"+description+"</p>"

			name = comment.user.last_name + " " + comment.user.first_name
			username = comment.user.username

			profile = get_id_profile(comment.user.id)
			photo = get_photo_profile(profile)
			if photo:
				path_img = settings.MEDIA_URL + str(photo)
			else:
				path_img = static("img/profile.png")
			img = "<img src='"+path_img+"' width=30 height=30 class='img-circle' />"
			html += "<a href='/profile/"+username+"'><p>"+ img + " " +  name +"</p></a>"
		except Comment.DoesNotExist:
			html = ""
	else:
		html = ""

	return html
