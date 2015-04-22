#encoding:utf-8 

from django import forms

from apps.profiles.models import Profile
'''
	Form of profile
'''
class FormProfile(forms.ModelForm):

	class Meta:
		model = Profile
		exclude = ('iduser', "idprofile")

	def __init__(self, *args, **kwargs):

		super(FormProfile, self).__init__(*args, **kwargs)
		class_css = 'form-control'

		for key in self.fields:
			if key != 'photo':
				self.fields[key].required = True
				self.fields[key].widget.attrs['class'] = class_css