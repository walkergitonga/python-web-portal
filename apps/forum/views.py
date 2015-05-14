# -*- coding: UTF-8 -*-
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import View
from django.views.generic.edit import FormView
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from log.utils import set_error_to_log

from apps.utils import helper_paginator
from apps.forum.models import Category, Forum, Topic


class ForumsView(View):
	'''
	This view display all forum registered
	'''
	template_name = "forum/index.html"

	def get(self, request, *args, **kwargs):

		categories = Category.objects.filter(hidden=False)

		data = {'categories': categories}

		return render(request, self.template_name, data)


class ForumView(View):
	'''
	This view display one forum registered
	'''
	template_name = "forum/forum.html"

	def get(self, request, forum, *args, **kwargs):

		forum = get_object_or_404(Forum, name=forum, hidden=False)
		topics = Topic.objects.filter(forum_id=forum.idforum)

		pag = helper_paginator(self, request, topics, 15, 'topics')

		data = {
			'forum': forum,
			'topics': pag['topics'],
			'paginator': pag
		}

		return render(request, self.template_name, data)


class TopicView(View):
	'''
	This view display one Topic of forum
	'''
	template_name = "forum/topic.html"

	def get(self, request, forum, slug, idtopic, *args, **kwargs):

		forum = get_object_or_404(Forum, name=forum, hidden=False)
		topic = get_object_or_404(Topic, idtopic=idtopic, slug=slug)

		data = {
			'topic': topic,
		}

		return render(request, self.template_name, data)