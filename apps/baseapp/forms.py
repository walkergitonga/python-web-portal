#encoding:utf-8 
from django import forms
from django.utils.translation import ugettext_lazy as _

'''
	Form of login
'''
class FormLogin(forms.Form):

	widgetUserEmail = forms.TextInput(attrs={'class': 'form-control', 
							'placeholder': _("Username or Email")})
	widgetPass = forms.PasswordInput(attrs={'class': 'form-control', 
						'placeholder':  _("Password")})

	user_email = forms.EmailField(max_length=45, widget=widgetUserEmail, 
									required=True)
	password = forms.CharField(max_length=45, widget=widgetPass, 
									required=True)