# -*- coding: UTF-8 -*-
import datetime

from django.db.models import get_model
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.template import defaultfilters
from django.views.generic import View
from django.views.generic.edit import FormView
from django.utils.crypto import get_random_string
from django.utils.html import strip_tags

from django.utils.translation import ugettext_lazy as _

from endless_pagination.decorators import page_template
from log.utils import set_error_to_log

from apps.forum.forms import (
	FormAddTopic, FormEditTopic,
	FormAddComment
)
from apps.forum.models import Category, Forum, Topic, Comment
from apps.forum.settings import (
	APP_PROFILE, MODEL_PROFILE,
	URL_PROFILE, FIELD_PHOTO_PROFILE
)
from apps.forum.utils import remove_folder_attachment
from apps.utils import (
	remove_file, helper_paginator, 
	get_route_file, remove_folder,
	exists_folder
)


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


@page_template('forum/topic.html')
def TopicView(request, forum, slug, idtopic, template='forum/topic_index.html', extra_context=None, *args, **kwargs):
	'''
	This view display one Topic of forum
	'''

	forum = get_object_or_404(Forum, name=forum, hidden=False)
	topic = get_object_or_404(Topic, idtopic=idtopic, slug=slug)

	Profile = get_model(APP_PROFILE, MODEL_PROFILE)

	profile = get_object_or_404(Profile, iduser_id=topic.user_id)
	field_photo = getattr(profile, FIELD_PHOTO_PROFILE)

	form_comment = FormAddComment()

	comments = Comment.objects.filter(topic_id=idtopic)

	data = {
		'topic': topic,
		'profile': profile,
		'URL_PROFILE': URL_PROFILE,
		'field_photo': field_photo,
		'form_comment': form_comment,
		'comments': comments,
	}

	if extra_context is not None:
		data.update(extra_context)
	return render(request, template, data)


class NewTopicView(FormView):
	'''
		This view allowed add new topic
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

		form = FormAddTopic(request.POST, request.FILES)

		if form.is_valid():
			obj = form.save(commit=False)

			now = datetime.datetime.now()
			user = User.objects.get(id=request.user.id)
			forum = get_object_or_404(Forum, name=forum)
			title = strip_tags(request.POST['title'])
			
			obj.date = now
			obj.user = user
			obj.forum = forum
			obj.title = title
			obj.slug = defaultfilters.slugify(request.POST['title'])

			if 'attachment' in request.FILES:
				id_attachment = get_random_string(length=32)
				obj.id_attachment = id_attachment

				file_name = request.FILES['attachment']
				obj.attachment = file_name

			obj.save()
			return self.form_valid(form, **kwargs)
		else:
			messages.error(request, _("Form invalid"))
			return self.form_invalid(form, **kwargs)


class EditTopicView(FormView):
	'''
		This view allowed edit topic
	'''
	template_name = "forum/edit_topic.html"
	form_class = FormEditTopic

	def get_success_url(self):
		return '/forum/' + self.kwargs['forum']

	def get(self, request, forum, idtopic, *args, **kwargs):
		
		topic = get_object_or_404(Topic, idtopic=idtopic, user_id=request.user.id)

		# Init fields form
		form = FormEditTopic(instance=topic)

		data = {
			'form': form,
			'topic': topic,
		}

		return render(request, self.template_name, data)

	def post(self, request, forum, idtopic, *args, **kwargs):

		topic = get_object_or_404(Topic, idtopic=idtopic, user_id=request.user.id)
		file_name = topic.attachment

		form = FormEditTopic(request.POST, request.FILES, instance=topic)
		file_path = settings.MEDIA_ROOT

		if form.is_valid():

			obj = form.save(commit=False)

			title = strip_tags(request.POST['title'])
			description = strip_tags(request.POST['description'])
			slug = defaultfilters.slugify(request.POST['title'])

			obj.title = title
			obj.description = description
			obj.slug = slug

			# If check field clear, remove file when update 
			if 'attachment-clear' in request.POST:
				route_file = get_route_file(file_path, file_name.name)

				try:
					remove_file(route_file)
				except Exception:
					pass

			if 'attachment' in request.FILES:

				if not topic.id_attachment:
					id_attachment = get_random_string(length=32)
					obj.id_attachment = id_attachment

				file_name_post = request.FILES['attachment']
				obj.attachment = file_name_post

				# Route previous file
				route_file = get_route_file(file_path, file_name.name)

				try:
					# If a previous file exists it removed
					remove_file(route_file)
				except Exception:
					pass

			# Update topic
			form.save()
			
			return self.form_valid(form, **kwargs)
		else:
			messages.error(request, _("Form invalid"))
			return self.form_invalid(form, **kwargs)


class DeleteTopicView(View):
	'''
	This view will delete one topic
	'''
	def get(self, request, forum, idtopic, *args, **kwargs):

		# Previouly verify that exists the topic
		topic = get_object_or_404(Topic, idtopic=idtopic, user_id=request.user.id)

		iduser_topic = topic.user_id

		# If my user delete
		if request.user.id == iduser_topic:
			remove_folder_attachment(idtopic)
			Topic.objects.filter(idtopic=idtopic, user_id=iduser_topic).delete()
		else:
			error = ""
			error = error + 'The user ' + str(request.user.id)
			error = error + ' He is trying to remove the job ' + str(idtopic)
			error = error +	' of user ' + str(iduser_topic)

			set_error_to_log(request, error)
			raise Http404

		return redirect('forum', forum)


class NewCommentView(View):
	'''
		This view allowed add new comment to topic
	'''
	def get(self, request, forum, slug, idtopic, *args, **kwargs):
		raise Http404()

	def post(self, request, forum, slug, idtopic, *args, **kwargs):

		form = FormAddComment(request.POST)

		param = ""
		param = forum + "/" + slug 
		param = param + "/" + str(idtopic) + "/"
		url = '/topic/' + param

		if form.is_valid():
			obj = form.save(commit=False)

			now = datetime.datetime.now()
			user = User.objects.get(id=request.user.id)
			topic = get_object_or_404(Topic, idtopic=idtopic)
			
			obj.date = now
			obj.user = user
			obj.topic_id = topic.idtopic

			obj.save()
			return HttpResponseRedirect(url)
		else:
			messages.error(request, _("Field required"))
			return HttpResponseRedirect(url)


class EditCommentView(View):
	'''
		This view allowed edit comment to topic
	'''
	def get(self, request, forum, slug, idtopic, idcomment, *args, **kwargs):
		raise Http404()

	def post(self, request, forum, slug, idtopic, idcomment, *args, **kwargs):

		param = ""
		param = forum + "/" + slug 
		param = param + "/" + str(idtopic) + "/"
		url = '/topic/' + param

		description = request.POST.get('update_description')

		if description:
			
			iduser = request.user.id
			Comment.objects.filter(idcomment=idcomment, user=iduser).update(
				description=description
			)

			return HttpResponseRedirect(url)
		else:
			return HttpResponseRedirect(url)


class DeleteCommentView(View):
	'''
		This view allowed remove comment to topic
	'''
	def get(self, request, forum, slug, idtopic, idcomment, *args, **kwargs):
		raise Http404()

	def post(self, request, forum, slug, idtopic, idcomment, *args, **kwargs):

		param = ""
		param = forum + "/" + slug 
		param = param + "/" + str(idtopic) + "/"
		url = '/topic/' + param

		try:
			iduser = request.user.id
			Comment.objects.filter(idcomment=idcomment, user=iduser).delete()

			return HttpResponseRedirect(url)
		except Exception:
			return HttpResponseRedirect(url)
