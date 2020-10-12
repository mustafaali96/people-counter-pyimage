from .libgenget import *
from .traverser import *



def create_catalogue(fname,catalogue_name):
	"""
	creates catalogue from directory scanning or txt_file reading which can be used to download book
	input: fname, if fname is directory then, catalogue is created by traversal
				  if fname is file name, then catalogue is created by reading txt file
	output: none
	"""
	if os.path.isfile(fname):
		create_catalogue_txt(fname,catalogue_name)
	else:
		create_catalogue_traversing(fname,catalogue_name)


def create_library(catalogue_name):
	"""
	creates a cataglogue using a catalogue file ( obj )
	input: catalogue name

	"""
	traverse_catalogue(catalogue_name,get_book)


def get_book_libgen(book_name,path='',auto=True):
	"""
	for downloading signle book from libgen.
	path: is including file name.
	input: book name
	"""
	get_book(book_name,path,auto=auto)







