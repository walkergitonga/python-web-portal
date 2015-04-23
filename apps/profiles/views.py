# -*- coding: UTF-8 -*-

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django.views.generic.edit import FormView

from apps.profiles.forms import FormProfile
from apps.profiles.models import Profile
from apps.utils import remove_file

class ProfileView(View):

	template_name = "profiles/profile.html"

	def get(self, request, *args, **kwargs):

		profile = Profile.objects.get(iduser_id=self.request.user.id)

		form = FormProfile(initial={
					"location": profile.location,
					"company": profile.company
				})

		return render(request, self.template_name,
					{'form': form, 'profile': profile})

class EditProfileView(FormView):

	template_name = "profiles/edit_profile.html"
	form_class = FormProfile
	success_url = '/edit_profile/'

	def get(self, request, *args, **kwargs):

		profile = Profile.objects.get(iduser_id=self.request.user.id)

		form = FormProfile(initial={
					"location": profile.location,
					"company": profile.company
				})

		return render(request, self.template_name,
					{'form': form, 'profile': profile})

	def post(self, request, *args, **kwargs):

		instance = Profile.objects.get(iduser_id=request.user.id)
		form = FormProfile(request.POST, request.FILES, instance=instance)

		file_name = instance.photo
		file_path = settings.MEDIA_ROOT

		if form.is_valid():

			if 'photo' in request.FILES:
				photo = request.FILES['photo']

				#Route previous file, if not exists display error
				try:
					route_file = file_path + "/" + file_name.name
				except Exception:
					pass

				try:
					#If a previous file exists it removed
					remove_file(route_file)
				except Exception:
					pass

			else:
				photo = ""
			
			form.photo = photo
			form.save()

			messages.success(request, _("Changes saved correctly"))
			return self.form_valid(form, **kwargs)

		else:
			messages.error(request, _("Form invalid"))
			return self.form_invalid(form, **kwargs)


