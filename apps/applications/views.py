# -*- coding: UTF-8 -*-
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django.views.generic.edit import FormView

from apps.applications.models import Applications
from apps.applications.forms import FormAddApplication

'''
	This view display the view
	for display applicatios
'''
class ApplicationsView(View):

	template_name = "applications/applications.html"

	def get(self, request, *args, **kwargs):

		apps = Applications.objects.all()

		return render(request, self.template_name, 
						{'apps': apps})

'''
	This view display the form for
	create one new application
'''
class ApplicationsAddView(FormView):

	template_name = "applications/add.html"
	form_class = FormAddApplication
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