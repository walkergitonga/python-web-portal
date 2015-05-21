from django.contrib import admin, messages
from django.shortcuts import get_object_or_404
from django.utils.translation import ugettext_lazy as _

from apps.forum.forms import FormAdminTopic
from apps.forum.models import (
	Category, Forum, 
	Topic, Comment
)
from apps.utils import (
	remove_folder, exists_folder, 
	get_folder_attachment
)


class TopicAdmin(admin.ModelAdmin):
	form = FormAdminTopic
	list_display = ('title', 'forum', 'date')
	list_filter = ['title', 'date']
	search_fields = ['title']
	actions=['delete']

	def get_actions(self, request):
		actions = super(TopicAdmin, self).get_actions(request)
		if 'delete_selected' in actions:
			del actions['delete_selected']
		return actions

	def delete(self, request, queryset):
		# Subtract one topic
		idtopic = request.POST.get('_selected_action')
		topic = get_object_or_404(Topic, idtopic=idtopic)
		forum = get_object_or_404(Forum, name=topic.forum, hidden=False)
		tot = forum.topics_count
		tot = tot - 1
		Forum.objects.filter(name=topic.forum, hidden=False).update(
			topics_count=tot
		)

		# Delete record
		for obj in queryset:
			obj.delete()

		path = get_folder_attachment(topic)
			
		# Remove attachment if exists
		if exists_folder(path):
			remove_folder(path)

		n = queryset.count()
		self.message_user(request, _("Successfully deleted %(count)d record/s.") % {
                "count": n, }, messages.SUCCESS)
	delete.short_description = _("Delete selected %(verbose_name_plural)s")
			
	
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
