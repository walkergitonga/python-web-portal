# -*- coding: UTF-8 -*-

from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView

from apps.profiles.forms import FormProfile
from apps.profiles.models import Profile

# Create your views here.
class ProfileView(FormView):

	template_name = "profiles/profile.html"
	form_class = FormProfile
	success_url = '/profile/'

	def get(self, request, *args, **kwargs):

		profile = Profile.objects.get(iduser_id=self.request.user.id)
		return render(request, self.template_name,
					{'form': self.form_class, 'profile': profile})

	def post(self, request, *args, **kwargs):

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		if form.is_valid():
			photo = request.FILES['photo']
			location = request.POST['location']
			company = request.POST['company']

			Profile.objects.filter(iduser_id=self.request.user.id).update(
									photo=photo, location=location, 
									company=company
								)

			messages.success(request, _("Changes saved correctly"))
			return self.form_valid(form, **kwargs)

		else:
			messages.error(request, _("Form invalid"))
			return self.form_invalid(form, **kwargs)


