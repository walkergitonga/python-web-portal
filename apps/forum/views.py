# -*- coding: UTF-8 -*-
import datetime

from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template import defaultfilters
from django.views.generic import View
from django.views.generic.edit import FormView
from django.utils.html import strip_tags

from django.utils.translation import ugettext_lazy as _

from log.utils import set_error_to_log

from apps.forum.forms import FormAddTopic
from apps.forum.models import Category, Forum, Topic
from apps.profiles.models import Profile
from apps.utils import helper_paginator


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
		profile = get_object_or_404(Profile, iduser_id=topic.user_id)

		data = {
			'topic': topic,
			'profile': profile,
		}

		return render(request, self.template_name, data)


class NewTopicView(FormView):
	'''
		This view allowe add new topic
	'''
	template_name = "forum/new_topic.html"
	form_class = FormAddTopic

	def get_success_url(self):
		return '/forum/' + self.kwargs['forum']

	def get(self, request, forum, *args, **kwargs):
		
		data = {
			'form': self.form_class,
			'forum': forum,
		}
		return render(request, self.template_name, data)

	def post(self, request, forum, *args, **kwargs):

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		if form.is_valid():
			obj = form.save(commit=False)

			now = datetime.datetime.now()
			user = User.objects.get(id=request.user.id)
			forum = get_object_or_404(Forum, name=forum)

			obj.date = now
			obj.user = user
			obj.forum = forum
			obj.slug = defaultfilters.slugify(request.POST['title'])

			obj.save()
			return self.form_valid(form, **kwargs)
		else:
			messages.error(request, _("Form invalid"))
			return self.form_invalid(form, **kwargs)
