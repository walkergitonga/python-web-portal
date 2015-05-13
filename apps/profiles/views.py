# -*- coding: UTF-8 -*-
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.generic import View
from django.views.generic.edit import FormView

from apps.profiles.forms import FormProfile, AdminProfileForm
from apps.profiles.models import Profile
from apps.utils import remove_file, helper_paginator


class ProfileView(View):
	'''
	This view contains the form
	of profile of user
	'''
	template_name = "profiles/profile.html"

	def get(self, request, username, *args, **kwargs):

		us = User.objects.get(username=username)
		iduser = us.id
		profile = Profile.objects.get(iduser_id=iduser)

		data = {'profile': profile}

		return render(request, self.template_name, data)


class EditProfileView(FormView):
	'''
	This view contains the form
	for edit profile
	'''
	template_name = "profiles/settings.html"
	form_class = FormProfile
	success_url = '/settings/edit_profile/'

	def get(self, request, *args, **kwargs):

		profile = Profile.objects.get(iduser_id=self.request.user.id)

		form = FormProfile(initial={
					"location": profile.location,
					"company": profile.company,
					"about": profile.about
				})

		data = {'form': form, 'profile': profile}

		return render(request, self.template_name, data)

	def post(self, request, *args, **kwargs):

		instance = Profile.objects.get(iduser_id=request.user.id)
		form = FormProfile(request.POST, request.FILES, instance=instance)

		file_name = instance.photo
		file_path = settings.MEDIA_ROOT

		if form.is_valid():

			if 'photo' in request.FILES:
				photo = request.FILES['photo']

				# Route previous file, if not exists display error
				try:
					route_file = file_path + "/" + file_name.name
				except Exception:
					pass

				try:
					# If a previous file exists it removed
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


class AdminView(FormView):
	'''
	This view is part of the section of
	settings, for change password
	'''
	template_name = "profiles/settings.html"
	form_class = AdminProfileForm
	success_url = '/settings/admin/'

	def post(self, request, *args, **kwargs):

		form_class = self.get_form_class()
		form = self.get_form(form_class)

		if form.is_valid():

			password = request.POST['password']
			new_password = request.POST['new_password']
			new_password2 = request.POST['new_password2']

			if not request.user.check_password(password):
				messages.error(request, _("Current password incorrect"))
				return self.form_invalid(form, **kwargs)

			if new_password != new_password2:
				messages.error(request, _("New password do not match"))
				return self.form_invalid(form, **kwargs)

			# Save new password
			new_password = make_password(new_password)
			User.objects.filter(id=request.user.id).update(
										password=new_password
									)

			return self.form_valid(form, **kwargs)
		else:
			messages.error(request, _("Form invalid"))
			return self.form_invalid(form, **kwargs)


class UsersView(View):
	'''
	This view display all profiles
	'''
	template_name = "profiles/users.html"

	def get(self, request, *args, **kwargs):

		iduser = request.user.id
		if iduser is None:
			profiles = Profile.objects.all()
		else:
			profiles = Profile.objects.filter(~Q(iduser_id=iduser))

		pag = helper_paginator(self, request, profiles, 12, 'profiles')

		data = {
				'profiles': pag['profiles'],
				'paginator': pag
			}

		return render(request, self.template_name, data)
