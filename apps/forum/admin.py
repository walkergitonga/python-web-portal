from django.contrib import admin

from apps.forum.forms import FormAdminTopic
from apps.forum.models import (
	Category, Forum, 
	Topic, Comment
)


class TopicAdmin(admin.ModelAdmin):
	form = FormAdminTopic
	list_filter = ['title', 'date']
	search_fields = ['title']
	
	
class ForumAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'description')
	list_filter = ['name', 'category']
	search_fields = ['name']

	# TinyMCE
	class Media:
		js = ('/static/js/libs/tiny_mce/tiny_mce.js', '/static/js/textareas.js')


admin.site.register(Category)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment)
