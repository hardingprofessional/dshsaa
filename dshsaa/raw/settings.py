#! /usr/bin/env python3

"""
settings.py is an internal module to the raw package which addresses operating system specific architecture.
"""

print("running settings.py")

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
byte512 = c.c_char * 512
vector = c.c_double * 3

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
