#! /usr/bin/env python3

import raw.settings as settings
import ctypes as c
import pdb
print("running maindll.py")

C_MAINDLL = c.CDLL(settings.LIB_MAIN_NAME)

# The pattern for the rest of this file will be:
# 1. Set parameter types
# 2. Set return types
# 3. Define a python-friendly function

## DllMainInit
C_MAINDLL.DllMainInit.restype = c.c_int64
def DllMainInit():
	"""
	python:function:: DllMainInit()

	Inits a DLLMain wrapper object in memory

	:returns: ctypes.c_int64 maindll_handle: A 64 bit specialized integer used to help the other DLLs find the running instance of maindll

	"""
	maindll_handle = C_MAINDLL.DllMainInit()
	return maindll_handle


## OpenLogile
C_MAINDLL.OpenLogFile.restype = c.c_int
C_MAINDLL.OpenLogFile.argtypes = [c.c_char_p]
def OpenLogFile(logfile):
	"""
	python:function:: OpenLogFile

	Opens a log file that all objects connected to maindll will write to.
	:param str fname: name of the file to write to
	:return ctypes.c_int retcode: the return status of the linked function, 0 on success, <0 on various failures
	"""
	retcode = maindll.OpenLogFile(fname.encode())
	return retcode


