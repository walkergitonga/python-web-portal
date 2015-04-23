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
	initial = {"location": "Entro"}

	def get(self, request, *args, **kwargs):

		profile = Profile.objects.get(iduser_id=self.request.user.id)

		form = FormProfile(initial={
					"location": profile.location,
					"company": profile.company
				})

		return render(request, self.template_name,
					{'form': form, 'profile': profile})

	def post(self, request, *args, **kwargs):

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		if form.is_valid():

			try:
				photo = request.FILES['photo']
			except Exception:
				photo = ""
			
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


