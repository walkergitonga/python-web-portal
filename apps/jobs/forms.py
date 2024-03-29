# encoding:utf-8 

from django import forms
from django.utils.translation import ugettext_lazy as _

from apps.widgets import TextareaWidget
from apps.jobs.models import Jobs


class FormAddJob(forms.ModelForm):
	'''
	Form for create one new application
	'''

	class Meta:
		model = Jobs
		exclude = ('iduser', "idjob", "date")
		widgets = { 
			'description': TextareaWidget,
		}  

	def __init__(self, *args, **kwargs):

		super(FormAddJob, self).__init__(*args, **kwargs)
		class_css = 'form-control'

		for key in self.fields:
			if key != "company":
				self.fields[key].required = True
			else:
				self.fields[key].required = False
			self.fields[key].widget.attrs['class'] = class_css


class FormEditJob(forms.ModelForm):
	'''
	Form for edit one new job
	'''
	description = forms.CharField(widget=TextareaWidget)

	class Meta:
		model = Jobs
		exclude = ('iduser', "idjob", "date")

	def __init__(self, *args, **kwargs):

		super(FormEditJob, self).__init__(*args, **kwargs)
		class_css = 'form-control'

		for key in self.fields:
			self.fields[key].required = True
			self.fields[key].widget.attrs['class'] = class_css
