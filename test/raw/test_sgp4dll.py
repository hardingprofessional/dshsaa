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
		init_subdll(astrodll.AstroFuncInit)
		sgp4dll.Sgp4SetLicFilePath('./dshsaa/libdll/') #get the license before initing sgp4
		init_subdll(sgp4dll.Sgp4Init)
		
		# open a log file
		maindll.OpenLogFile('sgp4.log')
		
		# make a test satellite available for various testing functions
		line1 = '1 25544U 98067A   19311.39056523  .00000757  00000-0  21099-4 0  9992'
		line2 = '2 25544  51.6451  11.2360 0005828 238.9618 210.3569 15.50258526197470'
		generic_satKey = tledll.TleAddSatFrLines(line1, line2)
		if generic_satKey.value <= 0:
			raise Exception("Failed to init generic_satKey with code %i" % generic_satKey.value)
		else:
			self.generic_satKey = generic_satKey
		
		# Initialize that satellite in the TLE context
		retcode = sgp4dll.Sgp4InitSat(generic_satKey)
		if retcode != 0:
			raise Exception("Failed to init tle with code %i" % (retcode))
	
	##Sgp4GetInfo
	def test_Sgp4GetInfo(self):
		infoStr = sgp4dll.Sgp4GetInfo()
		self.assertTrue(infoStr)
		
	##Sgp4GetLicFilePath 
	def test_Sgp4GetLicFilePath(self):
		licFilePath = sgp4dll.Sgp4GetLicFilePath()
		
	##Sgp4GetPropOut
	def test_Sgp4GetPropOut(self):
		# propogate a satellite
		satKey = self.generic_satKey
		mse = 3600
		(retcode, ds50UTC, pos, vel, llh) = sgp4dll.Sgp4PropMse(satKey, mse)
		self.assertEqual(retcode, 0)
		
		# retrieve data
		for xf_Sgp4Out in [2,3,4]:
			(retcode, destArr) = sgp4dll.Sgp4GetPropOut(satKey, xf_Sgp4Out)
			print(destArr)
	
	
	##Sgp4Init
	##Sgp4InitSat 
	##Sgp4PosVelToKep 
	##Sgp4PropAll 
	##Sgp4PropDs50UTC 
	##Sgp4PropDs50UtcLLH 
	##Sgp4PropDs50UtcPos 
	
	##Sgp4PropMse
	def test_Sgp4PropMse(self):
		satKey = self.generic_satKey
		mse = 3600
		(retcode, ds50UTC, pos, vel, llh) = sgp4dll.Sgp4PropMse(satKey, mse)
		# pdb.set_trace()
	
	
	
	
	##Sgp4ReepochTLE 
	##Sgp4RemoveAllSats 
	##Sgp4RemoveSat 
	##Sgp4SetLicFilePath 


	def tearDown(self):
		tledll.TleRemoveAllSats()
		return None
