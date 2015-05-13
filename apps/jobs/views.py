# -*- coding: UTF-8 -*-
import datetime

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
from apps.jobs.models import Jobs
from apps.jobs.forms import FormAddJob, FormEditJob


class JobsView(View):
	'''
	This view display in template the jobs
	'''
	template_name = "jobs/jobs.html"

	def get(self, request, *args, **kwargs):

		jobs = Jobs.objects.all().order_by("-date")

		pag = helper_paginator(self, request, jobs, 15, 'jobs')

		data = {
			'jobs': pag['jobs'],
			'paginator': pag
		}

		return render(request, self.template_name, data)


class JobsAddView(FormView):
	'''
	This view display the form for
	create one new job
	'''
	template_name = "jobs/add.html"
	form_class = FormAddJob
	success_url = '/jobs/'

	def get(self, request, *args, **kwargs):
		data = {'form': self.form_class}
		return render(request, self.template_name, data)

	def post(self, request, *args, **kwargs):

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		if form.is_valid():
			iduser = request.user.id
			title = strip_tags(request.POST.get('title'))
			description = request.POST.get('description')
			company = strip_tags(request.POST.get('company'))
			country = request.POST.get('country')
			email = request.POST.get('email')
			labels = strip_tags(request.POST.get('labels'))
			date = datetime.datetime.now()

			job = Jobs(
				iduser_id=iduser, title=title, 
				description=description,
				country=country, company=company,
				email=email, labels=labels, date=date
			)

			job.save()
			return self.form_valid(form, **kwargs)
		else:
			messages.error(request, _("Form invalid"))
			return self.form_invalid(form, **kwargs)


class JobSeeView(View):
	'''
	This view display information of one job
	'''
	template_name = "jobs/view_job.html"

	def get(self, request, idjob, username, *args, **kwargs):

		try:
			us = User.objects.get(username=username)
			iduser = us.id
			job = Jobs.objects.get(idjob=idjob, iduser_id=iduser)
		except Exception:
			raise Http404

		data = {'job': job}

		return render(request, self.template_name, data)


class JobDeleteView(View):
	'''
	This view will delete one job
	'''
	def get(self, request, idjob, username, *args, **kwargs):

		# Previouly verify that exists the app
		us = get_object_or_404(User, username=username)
		iduser = us.id
		job = get_object_or_404(Jobs, idjob=idjob, iduser_id=iduser)

		iduser_job = job.iduser_id

		# If my user delete
		if request.user.id == iduser_job:
			Jobs.objects.filter(idjob=idjob, iduser_id=iduser).delete()
		else:
			error = ""
			error = error + 'The user ' + str(request.user.id)
			error = error + ' He is trying to remove the job ' + str(idjob)
			error = error +	' of user ' + str(iduser_job)

			set_error_to_log(request, error)
			raise Http404

		return HttpResponseRedirect("/jobs/")


class JobEditView(FormView):
	'''
	This view will update one job
	'''
	template_name = "jobs/edit.html"
	form_class = FormEditJob
	success_url = '/jobs/'

	def get(self, request, idjob, username, *args, **kwargs):
		
		us = get_object_or_404(User, username=username)
		iduser = us.id

		# Only the user that created the app
		if iduser == request.user.id:

			job = get_object_or_404(Jobs, idjob=idjob, iduser=iduser)

			form = FormEditJob(initial={
							'title': job.title, 
							'description': job.description, 
							'company': job.company,
							'country': job.country,
							'labels': job.labels,
							'email': job.email
						})

			data = {'form': form}

			return render(request, self.template_name, data)
		else:
			error = ""
			error = error + 'The user ' + str(request.user.id)
			error = error + ' He is trying to modify the application ' + str(idjob) 
			error = error +	' of user ' + str(iduser)

			set_error_to_log(request, error)
			raise Http404

	def post(self, request, idjob, username, *args, **kwargs):

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		if form.is_valid():
			try:
				iduser = request.user.id
				title = strip_tags(request.POST.get('title'))
				description = request.POST.get('description')
				company = strip_tags(request.POST.get('company'))
				country = request.POST.get('country')
				email = request.POST.get('email')
				labels = strip_tags(request.POST.get('labels'))

				Jobs.objects.filter(idjob=idjob, iduser=iduser).update(
						title=title, 
						description=description,
						country=country, company=company,
						email=email, labels=labels
					)
			except Exception:
				messages.error(request, _("Form invalid"))
				return self.form_invalid(form, **kwargs)

			return self.form_valid(form, **kwargs)
		else:
			messages.error(request, _("Form invalid"))
			return self.form_invalid(form, **kwargs)
