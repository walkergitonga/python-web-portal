from django import forms

'''
	Widget rich textarea
'''
class TextareaWidget(forms.Textarea):
    
    class Media:
		#tiny_mce
		js = ('/static/js/libs/tiny_mce/tiny_mce.js', '/static/js/textareas.js')