from django.contrib import admin

from apps.forum.models import (
	Category, Forum, 
	Post, Comment
)


class ForumAdmin(admin.ModelAdmin):
	list_display = ('name', 'category', 'description')
	list_filter = ['name', 'category']
	search_fields = ['name']

admin.site.register(Category)
admin.site.register(Forum, ForumAdmin)
admin.site.register(Post)
admin.site.register(Comment)
