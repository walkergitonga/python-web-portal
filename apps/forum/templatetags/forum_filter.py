# encoding:utf-8
from django import template

from django.contrib.contenttypes.models import ContentType

from hitcount.models import HitCount

from apps.forum.models import Comment, Forum, Topic
from apps.forum.templatetags.photo import get_photo

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
	content = Topic.objects.get(idtopic=idtopic)
	idobj = ContentType.objects.get_for_model(content)

	hit = HitCount.objects.get(
			object_pk=idtopic,
			content_type_id=idobj
		)

	try:
		total = hit.hits
	except Exception:
		total = 0

	return total


@register.filter
def get_tot_users_comments(idtopic):
	'''
	This tag filter return the total
	users of one topic
	'''
	users = Comment.objects.filter(
				topic_id=idtopic,
			)

	data = ""
	lista = []
	i = 0
	for user in users:
		usuario = user.user.username
		if usuario in lista or i == 0:
			photo = get_photo(user.user.id)

			tooltip = ""
			tooltip += "data-toggle='tooltip' data-placement='bottom'"
			tooltip += "title='"+ usuario +"'"
			data += "<a href='/profile/"+ usuario +"' "+tooltip+" >"
			data += "<img class='img-circle' src='"+str(photo)+"' "
			data += "width=30, height=30></a>"
		else:
			lista.append(usuario)

		i=i+1

	return data