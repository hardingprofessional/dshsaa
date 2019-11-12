#! /usr/bin/env python3
import unittest
from dshsaa.raw import maindll, envdll
from dshsaa.raw import settings
import pdb
import ctypes as c
import os #for cleaning up output files

class TestEnvDLL(unittest.TestCase):
	def setUp(self):
		self.maindll_handle = maindll.DllMainInit()
		self.envdll_retcode = envdll.EnvInit(self.maindll_handle)
		if self.envdll_retcode != 0:
			raise Exception("envdll init retcode was %i != 0" % (self.envdll_retcode))
		return None
	
	## EnvGetEarthShape
	def test_EnvGetEarthShape(self):
		earth_shape = envdll.EnvGetEarthShape()
			
	## EnvGetFkConst
	def test_EnvGetFkConst(self):
		for (val, xf_FkCon) in zip(['C1', 'C1_dot', 'THGR70'],[1, 2, 3]):
			fkcon = envdll.EnvGetFkConst(xf_FkCon)

	## EnvGetFkIdx
	def test_EnvGetFkIdx(self):
		fk_setting = envdll.EnvGetFkIdx()
		
	## EnvGetFkPtr
	def test_EnvGetFkPtr(self):
		fk_ptr = envdll.EnvGetFkPtr()
		
	## EnvGetGeoConst
	def test_EnvGetGeoConst(self):
		codes = range(1, 12)
		descriptors = ['FF',
				'J2',
				'J3',
				'J4',
				'KE (er^1.5/min)',
				'KMPER: Earth Radius (km/er)',
				'RPTIM: Earth rotation rate w.r.t. fixed equinox (rad/min)',
				'CK2: J2/2',
				'CK4: -3/8 j4',
				'KS2EK', 
				'THDOT (rad/m)']
		for (code, descriptor) in zip(codes, descriptors):
			value = envdll.EnvGetGeoConst(code)
	
	## EnvGetGeoIdx
	def test_EnvGetGeoIdx(self):
		valid_codes = [84, 96, 72, 2, 68, 5, 9]
		geo_idx = envdll.EnvGetGeoIdx()
		self.assertTrue(geo_idx in valid_codes)
	
	## EnvGetGeoStr
	def test_EnvGetGeoStr(self):
		valid_strings = ['WGS-84', 'EGM-96', 'WGS-72', 'JGM2', 'SEM68R', 'GEM5', 'GEM9']
		geo_str = envdll.EnvGetGeoStr()
		self.assertTrue(geo_str in valid_strings)

	## EnvGetInfo
	def test_EnvGetInfo(self):
		info = envdll.EnvGetInfo()

	## EnvInit
	def test_EnvInit(self):
		# If the setUp runs, then EnvInit is OK
		return None
	
	## EnvLoadFile
	def test_EnvLoadFile(self):
		envConstFile = './test/raw/test_EnvLoadFile'
		retcode = envdll.EnvLoadFile(envConstFile)
		self.assertTrue(retcode == 0)

	## EnvSaveFile
	def test_EnvSaveFile(self):
		envConstFile = './test/raw/test_EnvSaveFile'
		saveMode = 0
		saveForm = 0
		retcode = envdll.EnvSaveFile(envConstFile, saveMode, saveForm)
		self.assertTrue(retcode == 0)
		os.remove(envConstFile)

	## EnvSetEarthShape
	def test_EnvSetEarthShape(self):
		earth_shape = envdll.EnvGetEarthShape()
		if earth_shape == 1:
			earth_shape = 0
		else:
			earth_shape = 1
		envdll.EnvSetEarthShape(earth_shape)
		new_earth_shape = envdll.EnvGetEarthShape()
		self.assertEqual(earth_shape, new_earth_shape)
	
	
	## EnvSetFkIdx
	def test_EnvSetFkIds(self):
		old_fk = envdll.EnvGetFkIdx()
		if old_fk == 4:
			set_fk = 5
		else:
			set_fk = 4
		envdll.EnvSetFkIdx(set_fk)
		new_fk = envdll.EnvGetFkIdx()
		self.assertEqual(set_fk, new_fk)
		

	## EnvSetGeoIdx
	def test_EnvSetGeoIdx(self):
		valid_geos = [84, 96, 72, 2, 68, 5, 9]
		for geo in valid_geos:
			envdll.EnvSetGeoIdx(geo)
			self.assertEqual(geo, envdll.EnvGetGeoIdx())
		
	## EnvSetGeoStr
	def test_EnvSetGeoStr(self):
		valid_geos = ['WGS-84', 'EGM-96', 'WGS-72', 'JGM2', 'SEM68R', 'GEM5', 'GEM9']
		for geo in valid_geos:
			envdll.EnvSetGeoStr(geo)
			self.assertEqual(geo, envdll.EnvGetGeoStr())

	def tearDown(self):
		return None
		
		
