import unittest
import dshsaa.raw as raw
#! /usr/bin/env python3

import ctypes as c

class TestMainDLL(unittest.TestCase):

	def setUp(self):
		# init a maindll class object to work off of
		maindll = raw.maindll.DllMainInit()
		
	def test_DllMainInit(self):
		maindll = raw.maindll.DllMainInit()
		self.assertEqual(type(maindll), type(c.c_int64(5)))

	def tearDown(self):
		print("need to implement removal of log file")


if __name__ == '__main__':
	unittest.main()
