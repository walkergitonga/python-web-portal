# -*- coding: UTF-8 -*-

from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, View
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

class ResetPassView(View):

	def post(self, request, *args, **kwargs):

		if request.POST.has_key('email'):

			#email = request.POST['email']

			'''my_domain = "http://" + request.get_host() + "/"

	        email_main = settings.EMAIL_MAIN
	        msg = EmailMultiAlternatives(subject="Reset password",
	                from_email = 'Portal web python <'+email_main+'>',
	                to= [email])

	        email64 = base64.b64encode(email)

	        #Parametros para el html del email
	        email_data = {
	          'email64':email64,
	          'nombre_destino': nombre_destino,
	          'my_domain': my_domain,
	        }
	        email_data = RequestContext(request, email_data)

	        link = "<a href='/new_password/'>Link</a>" 
	        text_email = "<p>Reset password: Please enter to link: " + link + " </p>"

	        msg.attach_alternative(text_email, "text/html")
	        msg.send()'''
			
			messages.success(request, _("Please, check the email"))
			return HttpResponseRedirect("/login/")
		else:
			messages.error(request, _("Form invalid"))
			return HttpResponseRedirect("/login/")