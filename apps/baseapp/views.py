# -*- coding: UTF-8 -*-

from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from apps.baseapp.forms import FormLogin

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

