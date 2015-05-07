# -*- coding: UTF-8 -*-
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils.html import strip_tags
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django.views.generic.edit import FormView

from log.utils import set_error_to_log

from apps.utils import helper_paginator
from apps.applications.models import Applications
from apps.applications.forms import FormAddApplication, FormEditApplication

'''
	This view display the view
	for display applicatios
'''
class ApplicationsView(View):

	template_name = "applications/applications.html"

	def get(self, request, *args, **kwargs):

		apps = Applications.objects.all().order_by("name")

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
	form_class = FormAddApplication
	success_url = '/applications/'

	def get(self, request, *args, **kwargs):
		
		return render(request, self.template_name, 
						{'form': self.form_class})

	def post(self, request, *args, **kwargs):

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		if form.is_valid():
			name = strip_tags(request.POST['name'])	
			description = request.POST['description']	
			repository = strip_tags(request.POST['repository'])	

			app = Applications(name=name, description=description,
								iduser_id=request.user.id,
								repository=repository)
			app.save()

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
	form_class = FormEditApplication
	success_url = '/applications/'

	def get(self, request, name, username, *args, **kwargs):
		
		us = get_object_or_404(User, username=username)
		iduser = us.id

		#Only the user that created the app
		if iduser == request.user.id:

			app = get_object_or_404(Applications, name=name, iduser=iduser)
			form = FormEditApplication(initial={'name': app.name, 
							'description': app.description, 
							'repository': app.repository})

			return render(request, self.template_name, 
							{'form': form})
		else:
			error = ""
			error = error + 'The user ' + str(request.user.id)
			error = error + ' He is trying to modify the application ' + name 
			error = error +	' of user ' + str(iduser)

			set_error_to_log(request, error)
			raise Http404

	def post(self, request, name, username, *args, **kwargs):

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		if form.is_valid():
			name = request.POST['name']	
			description = request.POST['description']	
			repository = strip_tags(request.POST['repository'])	

			iduser = request.user.id
			try:
				Applications.objects.filter(name=name, 
					iduser_id=iduser).update(description=description,
					repository=repository)
			except Exception:
				messages.error(request, _("Form invalid"))
				return self.form_invalid(form, **kwargs)

			return self.form_valid(form, **kwargs)
		else:
			messages.error(request, _("Form invalid"))
			return self.form_invalid(form, **kwargs)

'''
	This view will delete one application
'''
class ApplicationDeleteView(View):

	def get(self, request, name, username, *args, **kwargs):

		#Previouly verify that exists the app
		us = get_object_or_404(User, username=username)
		iduser = us.id
		app = get_object_or_404(Applications, name=name, iduser_id=iduser)

		iduser_app = app.iduser_id

		#If my user delete
		if request.user.id == iduser_app:
			Applications.objects.filter(name=name, iduser_id=iduser).delete()
		else:
			error = ""
			error = error + 'The user ' + str(request.user.id)
			error = error + ' He is trying to remove the application ' + name 
			error = error +	' of user ' + str(iduser_app)

			set_error_to_log(request, error)
			raise Http404

		return HttpResponseRedirect("/applications/")