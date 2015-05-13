import os

from django.core.paginator import Paginator


def exists_folder(route):

	'''
	This method verify that exists 
	folder in base to route
	'''
	if os.path.exists(route):
		return True
	else:
		return False


def create_folder(route):

	'''
	This method create one 
	folder in base to route
	'''
	if not exists_folder(route):
		os.makedirs(route)


def remove_file(route_file):

	'''
	This method remove one file
	in base to route and image
	'''
	if route_file != "" and not route_file is None:
		if os.path.exists(route_file):
			os.remove(route_file)


def helper_paginator(self, request, model, tot_record, nonRecPag):

	'''
	This function is responsible of Pagination
	'''
	result_list = Paginator(model, tot_record)
	try:
		page = int(request.GET.get('page')); 
	except:
		page = 1

	if page <= 0:
		page = 1

	if(page > result_list.num_pages):
		page = result_list.num_pages

	if (result_list.num_pages >= page):
		pagina = result_list.page(page)
		Contexto = {
			nonRecPag: pagina.object_list, 
			'page': page, 
			'pages': result_list.num_pages, 
			'has_next': pagina.has_next(),
			'has_prev': pagina.has_previous(), 
			'next_page': page+1, 
			'prev_page': page-1, 
			'firstPage': 1,
		}
		return Contexto
