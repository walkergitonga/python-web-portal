#encoding:utf-8
from django import template

from apps.forum.models import Forum

register = template.Library()


'''
	This tag filter the forum for category
'''
@register.filter
def in_category(category):
	return Forum.objects.filter(category_id=category, 
								hidden=False)