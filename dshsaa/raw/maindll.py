#! /usr/bin/env python3

import dshsaa.raw.settings as settings
import ctypes as c
import pdb

C_MAINDLL = c.CDLL(settings.LIB_MAIN_NAME)

# The pattern for the rest of this file will be:
# 1. Set parameter types
# 2. Set return types
# 3. Define a python-friendly function

## CloseLogFile
def CloseLogFile():
	"""
	python:function:: CloseLogFile

	Closes the log file last opened by this process.
	"""
	C_MAINDLL.CloseLogFile()
	# function is void, no return statement

## DllMainGetInfo
C_MAINDLL.DllMainGetInfo.argtypes = [c.c_char_p]
def DllMainGetInfo():
	"""
	python:function::DllMainGetInfo

	Returns information about DllMain DLL

	:returns: string info: a regular python string describing DllMain DLL
	"""
	info = c.c_char_p(bytes(512))
	C_MAINDLL.DllMainGetInfo(info)
	info = settings.byte_to_str(info) 
	return info

## DllMainInit
C_MAINDLL.DllMainInit.restype = settings.stay_int64
def DllMainInit():
	"""
	python:function:: DllMainInit()

	Inits a DLLMain wrapper object in memory

	:returns: ctypes.c_int64 maindll_handle: A 64 bit specialized integer used to help the other DLLs find the running instance of maindll

	"""
	maindll_handle = C_MAINDLL.DllMainInit()
	return maindll_handle

## GetInitDllNames
C_MAINDLL.GetInitDllNames.argtypes = [c.c_char_p]
def GetInitDllNames():
	initdllnames = c.c_char_p(bytes(512))
	C_MAINDLL.GetInitDllNames(initdllnames)
	initdllnames = settings.byte_to_str(initdllnames)
	return initdllnames

## GetLastErrMsg
C_MAINDLL.GetLastErrMsg.argtypes = [c.c_char_p]
def GetLastErrMsg():
	lastErrMsg = c.c_char_p(bytes(128))
	C_MAINDLL.GetLastErrMsg(lastErrMsg)
	lastErrMsg = settings.byte_to_str(lastErrMsg)
	return lastErrMsg

## GetLastInfoMsg
C_MAINDLL.GetLastInfoMsg.argtypes = [c.c_char_p]
def GetLastInfoMsg():
	lastInfoMsg = c.c_char_p(bytes(128))
	C_MAINDLL.GetLastInfoMsg(lastInfoMsg)
	lastInfoMsg = settings.byte_to_str(lastInfoMsg)
	return lastInfoMsg

## LogMessage
C_MAINDLL.LogMessage.argtypes = [c.c_char_p]
def LogMessage(message):
	message = message.encode('ascii')
	message = settings.enforce_limit(message, 128)
	message = c.c_char_p(message)
	C_MAINDLL.LogMessage(message)

## OpenLogile
C_MAINDLL.OpenLogFile.restype = c.c_int
C_MAINDLL.OpenLogFile.argtypes = [c.c_char_p]
def OpenLogFile(logfile):
	"""
	python:function:: OpenLogFile

	Opens a log file that all objects connected to maindll will write to.
	:param str logfile: name of the file to write to
	:return ctypes.c_int retcode: the return status of the linked function, 0 on success, <0 on various failures
	"""
	logfile = logfile.encode('ascii')
	logfile = settings.enforce_limit(logfile, 128)
	logfile = c.c_char_p(logfile)
	retcode = C_MAINDLL.OpenLogFile(logfile)
	return retcode


