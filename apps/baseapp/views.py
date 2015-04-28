# -*- coding: UTF-8 -*-

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import (password_reset, password_reset_complete,
								password_reset_done, password_reset_confirm)
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

'''
	This view contains the form
	for reset password of user
'''
def reset_password(request):

	return password_reset(request, is_admin_site=False,
                   template_name='baseapp/password_reset_form.html',
                   email_template_name='baseapp/password_reset_email.html',
                   subject_template_name='baseapp/password_reset_subject.txt',
                   password_reset_form=PasswordResetForm,
                   token_generator=default_token_generator,
                   post_reset_redirect=None,
                   from_email=None,
                   current_app=None,
                   extra_context=None,
                   html_email_template_name=None)

'''
	This view display messages
	that successful send email
'''
def pass_reset_done(request):

	return password_reset_done(request,
                        template_name='baseapp/password_reset_done.html',
                        current_app=None, extra_context=None)

'''
	This view display form reset confirm pass
'''
def reset_pass_confirm(request, uidb64, token):

	return password_reset_confirm(request, uidb64=uidb64, token=token,
                           template_name='baseapp/password_reset_confirm.html',
                           token_generator=default_token_generator,
                           set_password_form=SetPasswordForm,
                           post_reset_redirect=None,
                           current_app=None, extra_context=None)


'''
	This view display messages
	that successful reset pass
'''
def reset_done_pass(request):

	return password_reset_complete(request,
                            template_name='baseapp/password_reset_complete.html',
                            current_app=None, extra_context=None)

