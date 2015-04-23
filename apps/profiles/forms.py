#encoding:utf-8 

from django import forms

from apps.profiles.models import Profile
from apps.widgets import TextareaWidget

'''
	Form of profile
'''
class FormProfile(forms.ModelForm):

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