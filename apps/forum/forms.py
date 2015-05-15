# encoding:utf-8 

from django import forms

from apps.widgets import TextareaWidget
from apps.forum.models import Topic


class FormAdminTopic(forms.ModelForm):
	'''
	Form for topic cadmin
	'''
	class Meta:
		model = Topic
		exclude = ('slug',)
		widgets = { 
			'description': TextareaWidget,
		}  


class FormAddTopic(forms.ModelForm):
	'''
	Form for create one new topic
	'''

	class Meta:
		model = Topic
		exclude = ('forum', "user", "slug", "date")
		widgets = { 
			'description': TextareaWidget,
		}  

	def __init__(self, *args, **kwargs):

		super(FormAddTopic, self).__init__(*args, **kwargs)
		class_css = 'form-control'

		for key in self.fields:
			if key != "attachment":
				self.fields[key].required = True
				self.fields[key].widget.attrs['class'] = class_css
			else:
				self.fields[key].required = False
			