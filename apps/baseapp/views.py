# -*- coding: UTF-8 -*-
from django.views.generic import TemplateView

'''
	Index main view
'''
class IndexView(TemplateView):

    template_name = "baseapp/index.html"

