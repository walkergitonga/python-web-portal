#encoding:utf-8 
from django import forms
from django.contrib.auth import authenticate
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
