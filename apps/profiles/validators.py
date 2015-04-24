import os

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

'''
	Function that valid extension
	when upload file in form
'''
def valid_extension(value):

	list_file_allow = ['.png', '.jpg', '.gif', 
						'.ico', '.jpeg', '.bmp']

	extension = os.path.splitext(os.path.basename(value.name))[1]

	if not extension in list_file_allow:
		message = _("Files allowed: jpg, png, gif, ico, bmp")
		raise ValidationError(message)