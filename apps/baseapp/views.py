# -*- coding: UTF-8 -*-

from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from apps.baseapp.forms import FormLogin, FormSignup

'''
	Index main view
'''
class IndexView(TemplateView):

	template_name = "baseapp/index.html"

'''
	This view make login
'''
class LoginView(FormView):

	template_name = "baseapp/login.html"
	form_class = FormLogin
	success_url = '/'

	def get(self, request, *args, **kwargs):

		if request.user.is_authenticated():
			return HttpResponseRedirect("/")
		else:
			return render(request, self.template_name, 
						{'form': self.form_class})

	def post(self, request, *args, **kwargs):

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		if not request.user.is_authenticated():

			if form.is_valid():
				user = form.form_authenticate()
				if user:
					login(request, user)
					return HttpResponseRedirect("/")
				else:
					return self.form_invalid(form, **kwargs)
			else:
				return self.form_invalid(form, **kwargs)
		else:
			return HttpResponseRedirect("/")

'''
	This view make logout
'''
def signout(request):
	
	logout(request)
 	return HttpResponseRedirect('/')

'''
	This view is responsible of 
	create one new user
'''
class SignupView(FormView):

	template_name = "baseapp/signup.html"
	form_class = FormSignup
	success_url = '/join/'

	def get(self, request, *args, **kwargs):

		if request.user.is_authenticated():
			return HttpResponseRedirect("/")
		else:
			return render(request, self.template_name, 
						{'form': self.form_class})

	def post(self, request, *args, **kwargs):

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		if not request.user.is_authenticated():

			if form.is_valid():
				form.create_user()
				messages.success(request, _("Registration was successful"))
				return self.form_valid(form, **kwargs)
			else:
				messages.error(request, _("Form invalid"))
				return self.form_invalid(form, **kwargs)
		else:
			return HttpResponseRedirect("/")