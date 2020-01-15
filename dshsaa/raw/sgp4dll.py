#! /user/bin/env python3
import unittest
from dshsaa.raw import settings, maindll, envdll, astrodll, timedll, tledll, sgp4dll
import ctypes as c
import pdb

class TestSgp4Dll(unittest.TestCase):
	def setUp(self):
		#init maindll
		self.maindll_handle = maindll.DllMainInit()
		
		# init other dlls
		def init_subdll(initer):
			retcode = initer(self.maindll_handle)
			if retcode != 0:
				raise Exception("Failed to init %s with error code %i" % ('initer.__name__', retcode))
		
		init_subdll(timedll.TimeFuncInit)
		init_subdll(tledll.TleInit)
		init_subdll(envdll.EnvInit)
