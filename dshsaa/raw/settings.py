#! /usr/bin/env python3

"""
settings.py is an internal module to the raw package which addresses operating system specific architecture.
"""
import os
import platform
import ctypes as c
import pdb

## Global Vars

# DLL File Names (set in start_<os>())
LIB_MAIN_NAME = None 
LIB_TIME_NAME = None
LIB_TLE_NAME = None
LIB_ENV_NAME = None
LIB_ASTRO_NAME = None
LIB_SGP4_NAME = None

## Useful ctypes data objects
double1 = c.c_double * 1
double3 = c.c_double * 3
double6 = c.c_double * 6
double10 = c.c_double * 10
double64 = c.c_double * 64
double128 = c.c_double * 128
double512 = c.c_double * 512
double6x6 = (c.c_double * 6) * 6
class stay_int64(c.c_int64):
	"""
	ctypes primitives are automatically converted into python primitives unless subclassed. In order to consistently type check int64 numerical types (used as memory handles), I subclassed c_int64 but changed no properties or methods
	"""

## Useful byte sequences
string_term = (0).to_bytes(1, byteorder='little') #terminates strings

## Useful ctypes conversion patterns
def byte_to_str(byte_obj):
	byte_obj = byte_obj.value
	byte_obj = byte_obj.decode('ascii')
	byte_obj = byte_obj.rstrip()
	return byte_obj
	
def str_to_byte(s, fixed_width=None, limit=None, terminator=None):
	"""
	python:function::str_to_byte
	converts a python string into a DLL compatible bytes object
	:param str s: the string that needs to be converted
	:param int fixed_width: if provided, specifies the length of the byte array, padding with zeroes if necessary
	:param int limit: if provided, specifies the limit to the length of the byte array, throwing an error if exceeded
	:param bytes terminator: if provided, terminates the byte object with the provided bytes object
	"""
	# s for "string" (not technically a reserved keyword, but too popular to risk using)
	if fixed_width and limit and fixed_width > limit:
		raise Exception("fixed_width argument of %i is greater than the limit argument of %i" % (fixed_width, limit))
	b = s.encode('ascii', 'strict') #'b' for byte (reserved keyword)
	if terminator:
		b = b + terminator
	if fixed_width: #many of our strings are fixed width
		if len(b) > fixed_width:
			raise Exception("input string \"%s\" converts to <%b> which exceeds fixed width of %i" % (s, b, fixed_width))
		if len(b) < fixed_width:
			b = b + bytes(fixed_width - len(b))
	if limit: #l for "length", as many of our strings are limited to a certain length
		if len(b) > limit:
			raise Exception("input string \"%s\" converts to <%b> which exceeds hard limit of %i" % (s, b, limit))
	return b

def str_to_c_char_p(s, fixed_width=None, limit=None, terminator=None):
	b = str_to_byte(s, fixed_width=fixed_width, limit=limit, terminator=terminator)
	m = c.c_char_p(b)
	return m

def array_to_list(vector_obj):
	# converts c.c_int[] and c.c_double[] arrays into lists
	# does NOT work for any other data types!
	new_list = []
	for item in vector_obj:
		new_list.append(item)
	return new_list
	
def array2d_to_list(ar):
	# converts a 2d ctypes array into a list of equal shape
	# only works for double and integer ctypes!
	ar_len_d1 = len(ar)
	ar_len_d2 = len(ar[0])
	for i in range(ar_len_d1):
		if len(ar[i]) != ar_len_d2:
			raise Exception("ar[%i] is of length %i, expecting %i" % (i, len(ar[i]), ar_len_d2))
	li = list()
	for i in range(ar_len_d1):
		li.append(list())
		for j in range(ar_len_d2):
			li[i].append(ar[i]._type_(ar[i][j]))
			li[i][j] = li[i][j].value
	return li

def list_to_array(li, ct=c.c_double):
	"""
	converts a python list of ints or floats into a ctypes array
	:param list li: a list of ints or floats to convert into a ctypes array
	:param ctype ct: a ctype type to cast the elements of li (defaults to c.c_double)
	:return ar: a ctypes array
	:rtype: a ctypes array equivalent to ``ct * len(li)``
	"""
	art = ct * len(li)
	ar = art()
	for i in range(len(li)):
		ar[i] = ct(li[i])
	return ar

def feed_list_into_array(li, ar):
	"""
	python:function:: feed_list_into_array
	feeds the contents of a python list into a ctypes array
	assums python list is of equal or lesser length than the ctypes array
	:param list li: a list of python elements 
	:param ctypes_array ar: a fully initialized ctype array
	:return ar: returns the fully initialized ctype array with the python list contents in it
	"""
	if len(li) > len(ar):
		raise Exception("feeding a list of greater length into a ctypes array of lesser length will result in a memory buffer overflow event")
	for i in range(len(li)):
		ar[i] = ar._type_(li[i])
	return ar

def feed_2d_list_into_array(li, ar):
	"""
	python:function:: feed_2d_list_into_array
	copies the contents of a 2D python list into a 2D ctypes array
	Assumes both list and array are rectangular and of equal dimension
	If arrays are _not_ rectangular, a memory leak could occur!
	Only tested to work with integers and floats mapped to c.c_double[m][n]
	Will throw exception if list is different size from the array
	:param list li: the list of data to feed into the array
	:param ctype[][] ar: the array to feed data into
	:return ctype[][] ar: the array that has been filled with data from li
	"""
	# first, determine the size of the list
	li_len_d1 = len(li)
	li_len_d2 = len(li[0])
	for i in range(li_len_d1):
		if len(li[i]) != li_len_d2:
			raise Exception("li is not a rectangular matrix")
	ar_len_d1 = len(ar)
	ar_len_d2 = len(ar[0])
	for i in range(ar_len_d1):
		if len(ar[i]) != ar_len_d2:
			raise Exception("ar is not a rectangular matrix")
	if li_len_d1 != ar_len_d1 or li_len_d2 != ar_len_d2:
		raise Exception("li[%i,%i] and ar[%i,%i] are not the same dimension" % (li_len_d1, li_len_d2, ar_len_d1, ar_len_d2))
	for i in range(li_len_d1):
		for j in range(ar_len_d2):
			ar[i][j] = ar[i]._type_(li[i][j])
	return ar
	

## 
def enforce_limit(byte_obj, length, terminator=True):
	"""
	python:function:: enforce_limit
	When sending byte strings to DLL, this function will trim any byte strings in excess of a specified limit and ensure they end in a proper terminator
	:param bytes byte_obj: The byte string we wish to limit in length
	:param terminator: if true, enforce last byte is \0, else leave last byte as is
	:return bytes byte_obj: The byte string trimmed to the appropriate length with the final address guaranteed to be \0
	"""
	if terminator:
		if len(byte_obj) >= length:
			byte_obj = byte_obj[0:length-1] + bytes(1)
	else:
		if len(byte_obj) > length:
			byte_obj = byte_obj[0:length]
	return byte_obj

## Start
# This set of functions sets important global variables based on operating system and environment conditions

def __start():
	# Determine the OS
	current_os = platform.system()

	# based on OS, run start_<os>()
	if current_os == 'Linux':
		__start_linux()
		return 1
	elif current_os == 'Windows':
		__start_windows()
		return 1
	elif current_os == 'Darwin':
		__start_darwin()
		return 1
	
def __start_linux():
	# address global variables
	global LIB_MAIN_NAME
	global LIB_TIME_NAME
	global LIB_TLE_NAME
	global LIB_ENV_NAME
	global LIB_ASTRO_NAME
	global LIB_SGP4_NAME

	# set global vars
	LIB_MAIN_NAME = 'libdllmain.so'
	LIB_TIME_NAME = 'libtimefunc.so'
	LIB_TLE_NAME = 'libtle.so'
	LIB_ENV_NAME = 'libenvconst.so'
	LIB_ASTRO_NAME = 'libastrofunc.so'
	LIB_SGP4_NAME = 'libsgp4prop.so'

	# verify that 'LD_LIBRARY_PATH' is set _or_ that the requested 
	# .so files are available 
	# Note: until we make an installable package, there is no other 
	# way to get the so files
	if 'LD_LIBRARY_PATH' not in os.environ:
		print("Set LD_LIBRARY_PATH before running")
		exit(0) #standard exit

def __start_windows():
	# address global variables
	global LIB_MAIN_NAME
	global LIB_TIME_NAME
	global LIB_TLE_NAME
	global LIB_ENV_NAME
	global LIB_ASTRO_NAME
	global LIB_SGP4_NAME
	
	# set blobal variables
	LIB_MAIN_NAME = 'DllMain.dll'
	LIB_TIME_NAME = 'TimeFunc.dll'
	LIB_TLE_NAME = 'Tle.dll'
	LIB_ENV_NAME = 'EnvConst.dll'
	LIB_ASTRO_NAME = 'AstroFunc.dll'
	LIB_SGP4_NAME = 'Sgp4Prop.dll'

def __start_darwin():
	raise Exception('Code not started for MacOS/Darwin')

__start()
