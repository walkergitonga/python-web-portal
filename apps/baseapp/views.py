# -*- coding: UTF-8 -*-

from django.contrib.auth import authenticate, login as auth_login, logout
from django.http import Http404, HttpResponseRedirect
from django.views.generic import View
from django.views.generic.edit import FormView

from apps.baseapp.forms import FormLogin

'''
	Index main view
'''
class IndexView(FormView):

	template_name = "baseapp/index.html"
	form_class = FormLogin
	success_url = '/'

'''
	This view make login
'''
class LoginView(View):

	def get(self, request):
		raise Http404("Request incorrect")

	def post(self, request):

		if not request.user.is_authenticated():

			user_email = request.POST['user_email']
			password = request.POST['password']

			#If user you have access
			user = authenticate(username=user_email, password=password)
			#If user exists
			if user is not None:
				if user.is_active:
					auth_login(request, user)

		return HttpResponseRedirect("/")

'''
	This view make logout
'''
def signout(request):
	
	logout(request)
 	return HttpResponseRedirect('/')

