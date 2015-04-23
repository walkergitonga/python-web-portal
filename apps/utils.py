import os

'''
	This method verify that exists 
	folder in base to route
'''
def exists_folder(route):

	if os.path.exists(route):
		return True
	else:
		return False

'''
	This method create one 
	folder in base to route
'''
def create_folder(route):

	if not exists_folder(route):
		os.makedirs(route)

'''
	This method remove one file
	in base to route and image
'''
def remove_file(route_file):

	if route_file != "" and not route_file is None:
		if os.path.exists(route_file):
			os.remove(route_file)