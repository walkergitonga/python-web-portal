# -*- coding: UTF-8 -*-
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django.views.generic.edit import FormView

from apps.utils import helper_paginator
from apps.applications.models import Applications
from apps.applications.forms import FormApplication

'''
	This view display the view
	for display applicatios
'''
class ApplicationsView(View):

	template_name = "applications/applications.html"

	def get(self, request, *args, **kwargs):

		apps = Applications.objects.all()

		pag = helper_paginator(self, request, apps, 15, 'apps')

		return render(request, self.template_name, 
						{'apps': pag['apps'],
						'paginator': pag})

'''
	This view display the form for
	create one new application
'''
class ApplicationsAddView(FormView):

	template_name = "applications/add.html"
	form_class = FormApplication
	success_url = '/applications/add/'

	def get(self, request, *args, **kwargs):
		
		return render(request, self.template_name, 
						{'form': self.form_class})

	def post(self, request, *args, **kwargs):

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		if form.is_valid():
			name = request.POST['name']	
			description = request.POST['description']	
			repository = request.POST['repository']	

			app = Applications(name=name, description=description,
								iduser_id=request.user.id,
								repository=repository)
			app.save()

			messages.success(request, _("Saved record"))
			return self.form_valid(form, **kwargs)
		else:
			messages.error(request, _("Form invalid"))
			return self.form_invalid(form, **kwargs)

'''
	This view display information of one app
'''
class ApplicationSeeView(View):

	template_name = "applications/view_app.html"

	def get(self, request, name, username, *args, **kwargs):

		try:
			us = User.objects.get(username=username)
			iduser = us.id
			app = Applications.objects.get(name=name, iduser_id=iduser)
		except Exception:
			raise Http404

		return render(request, self.template_name, 
						{'app': app})

'''
	This view will update one application
'''
class ApplicationEditView(FormView):

	template_name = "applications/edit.html"
	form_class = FormApplication
	success_url = '/applications/'

	def get(self, request, name, username, *args, **kwargs):
		
		us = get_object_or_404(User, username=username)
		iduser = us.id

		#Only the user that created the app
		if iduser == request.user.id:

			app = get_object_or_404(Applications, name=name, iduser=iduser)
			form = FormApplication(initial={'name': app.name, 
							'description': app.description, 
							'repository': app.repository})

			return render(request, self.template_name, 
							{'form': form, 'app': app})
		else:
			raise Http404

	def post(self, request, *args, **kwargs):

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		if form.is_valid():
			name = request.POST['name']	
			description = request.POST['description']	
			repository = request.POST['repository']	

			iduser = request.user.id
			try:
				Applications.objects.filter(name=name, 
					iduser_id=iduser).update(description=description,
					repository=repository)
			except Exception:
				messages.error(request, _("Form invalid"))
				return self.form_invalid(form, **kwargs)

			messages.success(request, _("Updated record"))
			return self.form_valid(form, **kwargs)
		else:
			messages.error(request, _("Form invalid"))
			return self.form_invalid(form, **kwargs)
