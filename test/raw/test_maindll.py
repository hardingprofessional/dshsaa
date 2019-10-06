#! /usr/bin/env python3
import unittest
from dshsaa.raw import maindll, timedll
from dshsaa.raw import settings
import pdb
import ctypes as c

class TestMainDLL(unittest.TestCase):

	def setUp(self):
		return None

	#def test_CloseLogFile():
	# not sure how to test that a file is closed	

	def test_DllMainGetInfo(self):
		info = maindll.DllMainGetInfo()
		self.assertEqual(type(info), str)

	def test_DllMainInit(self):
		maindll_handle = maindll.DllMainInit()
		self.assertEqual(type(maindll_handle), settings.stay_int64)

	def test_GetInitDllNames(self):
		initdllnames = maindll.GetInitDllNames()
		self.assertEqual(type(initdllnames), str)

	def test_GetLastErrMsg(self):
		lastErrMsg = maindll.GetLastErrMsg()
		self.assertEqual(type(lastErrMsg) , str)

	def test_GetInfoErrMsg(self):
		lastInfoMsg = maindll.GetLastInfoMsg()
		self.assertEqual(type(lastInfoMsg) , str)

#	def test_LogMessage(self):
#		message = "generic log message"
#		logfile = 

	def tearDown(self):
		return None
if __name__ == '__main__':
	unittest.main()
