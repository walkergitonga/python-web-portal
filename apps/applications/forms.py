# encoding:utf-8 

from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.widgets import TextareaWidget
from apps.applications.models import Applications


class FormAddApplication(forms.ModelForm):

	'''
	Form for create one new application
	'''
	description = forms.CharField(widget=TextareaWidget)

	class Meta:
		model = Applications
		exclude = ('iduser', "idapp")

	def __init__(self, *args, **kwargs):

		super(FormAddApplication, self).__init__(*args, **kwargs)
		class_css = 'form-control'

		for key in self.fields:
			self.fields[key].required = True
			self.fields[key].widget.attrs['class'] = class_css


class FormEditApplication(forms.ModelForm):

	'''
	Form for edit one new application
	'''
	description = forms.CharField(widget=TextareaWidget)

	class Meta:
		model = Applications
		exclude = ('iduser', "idapp")

	def __init__(self, *args, **kwargs):

		super(FormEditApplication, self).__init__(*args, **kwargs)
		class_css = 'form-control'

		for key in self.fields:
			self.fields[key].required = True
			self.fields[key].widget.attrs['class'] = class_css
			if key is "name":
				self.fields[key].widget.attrs['readonly'] = True
								
	def clean(self):

		try:
			self.cleaned_data['name']
		except Exception:
			raise forms.ValidationError(_("This field name is required"))
		
		try:
			self.cleaned_data['description']
		except Exception:
			raise forms.ValidationError(_("This field description is required"))
		
		try:
			self.cleaned_data['repository']
		except Exception:
			raise forms.ValidationError(_("This field repository is required"))
