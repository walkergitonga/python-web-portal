#encoding:utf-8 

from django import forms

from apps.widgets import TextareaWidget
from apps.applications.models import Applications

'''
	Form for create one new application
'''
class FormAddApplication(forms.ModelForm):

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
