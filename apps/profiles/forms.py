# encoding:utf-8 

from django import forms

from apps.profiles.models import Profile
from apps.widgets import TextareaWidget


class FormProfile(forms.ModelForm):

	'''
	Form of edit profile
	'''
	about = forms.CharField(widget=TextareaWidget)

	class Meta:
		model = Profile
		exclude = ('iduser', "idprofile")
		widgets = {
			'photo': forms.FileInput,
		}

	def __init__(self, *args, **kwargs):
		super(FormProfile, self).__init__(*args, **kwargs)

		class_css = 'form-control'
		for key in self.fields:
			if key != 'photo':
				self.fields[key].required = True
				self.fields[key].widget.attrs['class'] = class_css


class AdminProfileForm(forms.Form):

	'''
	Form of admin account profile
	'''
	widgetPass = forms.PasswordInput(attrs={'class': 'form-control'})

	password = forms.CharField(
					max_length=45, widget=widgetPass, required=True
				)
	new_password = forms.CharField(
						max_length=45, widget=widgetPass, required=True
					)
	new_password2 = forms.CharField(
						max_length=45, widget=widgetPass, required=True
					)
