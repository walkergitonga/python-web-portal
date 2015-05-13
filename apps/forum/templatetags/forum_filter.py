# encoding:utf-8
from django import template

from apps.forum.models import Forum

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
