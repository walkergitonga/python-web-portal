from django.contrib import admin
from django.shortcuts import get_object_or_404

from apps.forum.forms import FormAdminTopic
from apps.forum.models import (
	Category, Forum, 
	Topic, Comment
)


class TopicAdmin(admin.ModelAdmin):
	form = FormAdminTopic
	list_display = ('title', 'forum', 'date')
	list_filter = ['title', 'date']
	search_fields = ['title']
	actions=['delete']

	def get_actions(self, request):
		actions = super(TopicAdmin, self).get_actions(request)
		del actions['delete_selected']
		return actions

	def delete(self, request, queryset):
		idtopic = request.POST.get('_selected_action')
		topic = get_object_or_404(Topic, idtopic=idtopic)
		forum = get_object_or_404(Forum, name=topic.forum, hidden=False)
		tot = forum.topics_count
		tot = tot - 1
		Forum.objects.filter(name=topic.forum, hidden=False).update(
			topics_count=tot
		)

		for obj in queryset:
			obj.delete()
			
	
class ForumAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'description', 'topics_count')
	list_filter = ['name', 'category']
	search_fields = ['name']

	# TinyMCE
	class Media:
		js = ('/static/js/libs/tiny_mce/tiny_mce.js', '/static/js/textareas.js')


admin.site.register(Category)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Comment)
