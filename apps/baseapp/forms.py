#encoding:utf-8 
import datetime

from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

'''
	Form of login
'''
class FormLogin(forms.Form):

	widgetUserEmail = forms.TextInput(attrs={'class': 'form-control', 
							'placeholder': _("Username or Email")})
	widgetPass = forms.PasswordInput(attrs={'class': 'form-control', 
						'placeholder':  _("Password")})

	user_email = forms.CharField(max_length=45, widget=widgetUserEmail, 
									required=True)
	password = forms.CharField(max_length=45, widget=widgetPass, 
									required=True)

	'''
		This method if responsible of 
		authenticate user login, if ok
		then return the user
	'''
	def form_authenticate(self):

		user_email = self.cleaned_data.get('user_email')
		password = self.cleaned_data.get('password')

		user = authenticate(username=user_email, password=password)
		if user is None:
			error = ""
			error = error + "<ul class='errorlist'><li>"
			error = error + str(_("Incorrect username or password."))
			error = error + "</li></ul>"
			self._errors["password"] = error
		return user

'''
	Form for create one new user
'''
class FormSignup(forms.ModelForm):

	widget_pass = forms.PasswordInput(attrs={'class': 'form-control'})
	password = forms.CharField(label=_("Password"), max_length=45, 
								widget=widget_pass)
	password_confirm = forms.CharField(label=_("Repeat password"), max_length=45, 
								widget=widget_pass)

	class Meta:
		model = User
		fields = ['username', 'email', 'first_name', 'last_name']

	def __init__(self, *args, **kwargs):

		super(FormSignup, self).__init__(*args, **kwargs)
		class_css = 'form-control'

		for key in self.fields:
			self.fields[key].required = True
			self.fields[key].widget.attrs['class'] = class_css


	#Valid the passwords
	def clean_password_confirm(self):

		password1 = self.cleaned_data.get('password')
		password2 = self.cleaned_data.get('password_confirm')

		if password1 and password1 != password2:
			raise forms.ValidationError(_("Passwords don't match"))

		return self.cleaned_data

	#Valid the email that is unique
	def clean_email(self):

		email = self.cleaned_data.get('email')
		username = self.cleaned_data.get('username')
		if email and User.objects.filter(email=email).exclude(username=username).count():
			raise forms.ValidationError(_('Email addresses must be unique.'))
		return email

	#Create one new user 
	def create_user(self):
			
		username = self.cleaned_data.get('username')
		email = self.cleaned_data.get('email')
		first_name = self.cleaned_data.get('first_name')
		last_name = self.cleaned_data.get('last_name')
		password = self.cleaned_data.get('password')

		now = datetime.datetime.now()

		us = User(username=username, email=email,
			first_name=first_name, 
			last_name=last_name, is_active=True,
			is_superuser=False, date_joined=now,
			is_staff=False)

		us.set_password(password)
		us.save()