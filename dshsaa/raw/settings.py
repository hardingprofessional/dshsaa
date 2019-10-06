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
double512 = c.c_double * 512
vector = c.c_double * 3
class stay_int64(c.c_int64):
	"""
	ctypes primitives are automatically converted into python primitives unless subclassed. In order to consistently type check int64 numerical types, I subclassed c_int64 but changed no properties or methods
	"""
	

## Useful ctypes conversion patterns
def byte_to_str(byte_obj):
	byte_obj = byte_obj.value
	byte_obj = byte_obj.decode()
	byte_obj = byte_obj.rstrip()
	return byte_obj

def vector_to_list(vector_obj):
	return [float(vector_obj[0]), float(vector_obj[1]), float(vector_obj[2])]

def feed_list_into_array(li, ar):
	"""
	python:function:: feed_list_into_array
	feeds the contents of a python list into a ctypes array
	:param list li: a list of python elements 
	:param ctypes_array ar: a fully initialized ctype array
	:return ar: returns the fully initialized ctype array with the python list contents in it
	"""
	if len(li) > len(ar):
		raise Exception("feeding a list of greater length into a ctypes array of lesser length will result in a memory buffer overflow event")
	for i in range(len(li)):
		ar[i] = ar._type_(li[i])
	return ar
		

## 
def enforce_limit(byte_obj, length):
	if len(byte_obj) >= length-1:
		byte_obj = byte_obj[0:length-2] + bytes(1)
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
