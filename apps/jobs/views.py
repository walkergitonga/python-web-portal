# -*- coding: UTF-8 -*-
import datetime

from django.contrib import messages
from django.shortcuts import render
from django.views.generic import View
from django.views.generic.edit import FormView
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _

from apps.utils import helper_paginator
from apps.jobs.models import Jobs
from apps.jobs.forms import FormAddJob

'''
	This view display in template the jobs
'''
class JobsView(View):

	template_name = "jobs/jobs.html"

	def get(self, request, *args, **kwargs):

		jobs = Jobs.objects.all().order_by("date")

		pag = helper_paginator(self, request, jobs, 15, 'jobs')

		return render(request, self.template_name, 
						{'jobs': pag['jobs'],
						'paginator': pag})

'''
	This view display the form for
	create one new job
'''
class JobsAddView(FormView):

	template_name = "jobs/add.html"
	form_class = FormAddJob
	success_url = '/jobs/'

	def get(self, request, *args, **kwargs):
		
		return render(request, self.template_name, 
						{'form': self.form_class})

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

			job = Jobs(iduser_id=iduser, title=title, description=description,
					country=country, company=company,
					email=email, labels=labels, date=date)

			job.save()
			
			return self.form_valid(form, **kwargs)
		else:
			messages.error(request, _("Form invalid"))
			return self.form_invalid(form, **kwargs)