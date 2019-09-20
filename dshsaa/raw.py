#! /usr/bin/env python3

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

# DLL ctype objects (set in start_<os>())
C_MAINDLL = None
C_TIMEDLL = None
C_TLEDLL = None
C_ENVDLL = None
C_ASTRODLL = None
C_SGP4DLL = None

## Useful ctypes data objects
byte512 = c.c_char*512
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

	# init the ctypes objects
	__init_ctypes()

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

	# init the ctypes objects
	__init_ctypes()

def __start_darwin():
	raise Exception('Code not started for MacOS/Darwin')

def __init_ctypes():
	# address global variables
	global C_MAINDLL
	global C_MAINDLL
	global C_TIMEDLL
	global C_TLEDLL
	global C_ENVDLL
	global C_ASTRODLL
	global C_SGP4DLL

	# init the ctypes objects using global parameters
	C_MAINDLL = c.CDLL(LIB_MAIN_NAME)
	C_TIMEDLL = c.CDLL(LIB_TIME_NAME)
	C_TLEDLL = c.CDLL(LIB_TLE_NAME)
	C_ENVDLL = c.CDLL(LIB_ENV_NAME)
	C_ASTRODLL = c.CDLL(LIB_ASTRO_NAME)
	C_SGP4DLL = c.CDLL(LIB_SGP4_NAME)

	## C_MAINDLL argument and return types

	# C_MAINDLL.DllMainInit()
	C_MAINDLL.DllMainInit.restype = c.c_int64

	## C_MAINDLL.OpenLogFile
	C_MAINDLL.OpenLogFile.restype = c.c_int
	C_MAINDLL.OpenLogFile.argtypes = [c.c_char_p]

	# Nominal return
	return 1

class MainDLL:
	"""

	.. py:class:: MainDLL

	The MainDLL class and its methods are a way to directly access the SAA Main DLL dynamic link library / shared object file.

	An object-oriented approach was chosen so that multiple MainDLL objects could be implmeneted simultaneously.

	To use:
	maindll = new raw.MainDLL()
	maindll_handle = maindll.DllMainInit()
	"""
	def __init__(self):
		return None

	def DllMainInit(self):
		""" 
		.. py:method:: DllMainInit
		Initializes a DllMainInit C Object

		:returns: ctypes.c_int64 maindll_handle: A 64 bit specialized integer used to help the other DLLs find the running instance of maindll
		"""
		maindll_handle = C_MAINDLL.DllMainInit()
		return maindll_handle	

	def OpenLogFile(self, fname):
		""" 
        .. py:method:: OpenLogFile

		Opens a log file which will be used by maindll and all dll's inited with the maindll numerica handle.
		:param str fname: name of the file to write to
		:return ctypes.c_int retcode: the return status of the linked function
		"""
		retcode = maindll.OpenLogFile(fname.encode())
		return retcode


class timedll:
	"""
	This class contians the timedll dynamic link library / shared objects within its member methods.
	"""
	def __init__(self):
		return None


## run on start
# __start() #sets global variables and checks environment

if __name__ == "__main__":
	m = MainDLL()
	i = m.DllMainInit()
	pdb.set_trace()
	print("complete")
