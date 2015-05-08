#encoding:utf-8
from django import template

register = template.Library()


'''
	This tag generate the labels in
	base string separated for commas
'''
@register.simple_tag
def labels(value):
	
	html = ""

	listValue = value.split(",")
	for val in listValue:
		html = html + '<span class="label label-default">'+val+'</span> '

	return html