#! /usr/bin/env python3
import unittest
from dshsaa.raw import settings, maindll, envdll, timedll, tledll
import pdb
import ctypes as c 

class TestTleDll(unittest.TestCase):
	@classmethod
	def setUpClass(self):
		self.maindll_handle = maindll.DllMainInit()
		self.timedll_retcode = timedll.TimeFuncInit(self.maindll_handle)
		if self.timedll_retcode != 0:
			raise Exception("Failed to init timedll with error code %i" % self.timedll_retcode)
		self.tledll_retcode = tledll.TleInit(self.maindll_handle)
		if self.tledll_retcode != 0:
			raise Exception("Failed to init tledll with error code %i" % self.tledll_retcode)
		maindll.OpenLogFile('tle.log')

	def setUp(self):
		aline1 = '1 25544U 98067A   19311.39056523  .00000757  00000-0  21099-4 0  9992'
		aline2 = '2 25544  51.6451  11.2360 0005828 238.9618 210.3569 15.50258526197470'
		generic_satKey = tledll.TleAddSatFrLines(aline1, aline2)
		if generic_satKey.value <= 0:
			raise Exception("Failed to init generic_satKey with code %i" % generic_satKey.value)
		else:
			self.generic_satKey = generic_satKey

	##TleAddSatFrArray
	def test_TleAddSatFrArray(self):
		xa_tle = [90004.0, 19409.03935584, 1.327e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 64.7716, 194.9878, 0.6033327, 269.302, 18.611, 2.00615358, 3847.0, 0.0, 0.0, 0.0, 882.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
		xs_tle = 'USGP4-KNW'
		satKey = tledll.TleAddSatFrArray(xa_tle, xs_tle)
		self.assertTrue(satKey.value > 0)
		
	##TleAddSatFrArrayML
	def test_TleAddSatFrArrayML(self):
		xa_tle = [90004.0, 19409.03935584, 1.327e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 64.7716, 194.9878, 0.6033327, 269.302, 18.611, 2.00615358, 3847.0, 0.0, 0.0, 0.0, 882.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
		xs_tle = 'USGP4-KNW'
		satKey = tledll.TleAddSatFrArrayML(xa_tle, xs_tle)
		self.assertTrue(satKey.value > 0)
		
	##TleAddSatFrFieldsGP
	def test_TleAddSatFrFieldsGP(self):
		"""
		ISS (ZARYA)
		1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
		2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
		Notes:
		ISS (ZARYA) is an illegal name because it has > 8 characters
		bstar comes from digits "-11606-4". To apply leading zero use formula #0.[0]{n}(digits) to yield -0.000011606
		Eccentricity needs a leading "0."
		Docs: 
		https://en.wikipedia.org/wiki/Two-line_element_set#cite_note-nasahelp-12
		https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html
		"""
		satNum    = 25544
		secClass  = 'U'
		satName   = 'ISS'
		epochYr   = 8
		epochDays = 264.51782528
		bstar     = -0.000011606 #0.[0]{n}(digits) to accomplish assumed decimal point
		ephType   = 0
		elsetNum  = 292
		incli     = 51.6416
		node      = 247.4627
		eccen     = 0.0006703 #a leading decimal point is necessary
		omega     = 130.5360
		mnAnomaly = 325.0288
		mnMotion  = 15.72125391
		revNum    = 56353
		satKey    = tledll.TleAddSatFrFieldsGP(satNum, secClass, satName, epochYr, epochDays, bstar, ephType, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum)
		self.assertTrue(satKey.value > 0)
	
	##TleAddSatFrFieldsGP2
	def test_TleAddSatFrFieldsGP2(self):
		"""
		ISS (ZARYA)
		1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
		2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
		Notes:
		ISS (ZARYA) is an illegal name because it has > 8 characters
		bstar comes from digits "-11606-4". To apply leading zero use formula #0.[0]{n}(digits) to yield -0.000011606
		Eccentricity needs a leading "0."
		Docs: 
		https://en.wikipedia.org/wiki/Two-line_element_set#cite_note-nasahelp-12
		https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html
		"""
		satNum    = 25544
		secClass  = 'U'
		satName   = 'ISS'
		epochYr   = 8
		epochDays = 264.51782528
		bstar     = -0.000011606 #0.[0]{n}(digits) to accomplish assumed decimal point
		ephType   = 0
		elsetNum  = 292
		incli     = 51.6416
		node      = 247.4627
		eccen     = 0.0006703 #a leading decimal point is necessary
		omega     = 130.5360
		mnAnomaly = 325.0288
		mnMotion  = 15.72125391
		revNum    = 56353
		nDotO2    = 555555 #value not used, but is stored for data integrity
		n2DotO6   = 666666 #value not used, but is stored for data integrity
		satKey    = tledll.TleAddSatFrFieldsGP2(satNum, secClass, satName, epochYr, epochDays, bstar, ephType, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum, nDotO2, n2DotO6)
		self.assertTrue(satKey.value > 0)

	@unittest.skip("Segmentation fault, matlab")
	##TleAddSatFrFieldsGP2ML
	def test_TleAddSatFrFieldsGP2ML(self):
		"""
		ISS (ZARYA)
		1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
		2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
		Notes:
		ISS (ZARYA) is an illegal name because it has > 8 characters
		bstar comes from digits "-11606-4". To apply leading zero use formula #0.[0]{n}(digits) to yield -0.000011606
		Eccentricity needs a leading "0."
		Docs: 
		https://en.wikipedia.org/wiki/Two-line_element_set#cite_note-nasahelp-12
		https://spaceflight.nasa.gov/realdata/sightings/SSapplications/Post/JavaSSOP/SSOP_Help/tle_def.html
		"""
		satNum    = 25544
		secClass  = 'U'
		satName   = 'ISS'
		epochYr   = 8 #2008
		epochDays = 264.51782528
		bstar     = -0.000011606 #0.[0]{n}(digits) to accomplish assumed decimal point
		ephType   = 0
		elsetNum  = 292
		incli     = 51.6416
		node      = 247.4627
		eccen     = 0.0006703 #a leading decimal point is necessary
		omega     = 130.5360
		mnAnomaly = 325.0288
		mnMotion  = 15.72125391
		revNum    = 56353
		nDotO2    = 555555 #value not used, but is stored for data integrity
		n2DotO6   = 666666 #value not used, but is stored for data integrity
		satKey    = tledll.TleAddSatFrFieldsGP2ML(satNum, secClass, satName, epochYr, epochDays, bstar, ephType, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum, nDotO2, n2DotO6)
		self.assertTrue(satKey.value > 0)
	
	##TleAddSatFrFieldsSP
	def test_TleAddSatFrFieldsSP(self):
		"""
		https://www.sat.dundee.ac.uk/fle.html
		"""
		satNum    = 21263
		secClass  = 'U'
		satName   = 'Dundee'
		epochYr   = 94
		epochDays = 264.51782528
		bTerm     = 0.06822045
		ogParm    = 0.001
		agom      = .0000500000
		elsetNum  = 292
		incli     = 51.6416
		node      = 247.4627
		eccen     = 0.0006703
		omega     = 130.5360
		mnAnomaly = 325.0288
		mnMotion  = 15.72125391
		revNum    = 15390
		satKey    = tledll.TleAddSatFrFieldsSP(satNum, secClass, satName, epochYr, epochDays, bTerm, ogParm, agom, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum)
		self.assertTrue(satKey.value > 0)
		
	##TleAddSatFrFieldsSPML
	@unittest.skip("Segmentation fault, matlab")
	def test_TleAddSatFrFieldsSPML(self):
		"""
		https://www.sat.dundee.ac.uk/fle.html
		"""
		satNum    = 21263
		secClass  = 'U'
		satName   = 'Dundee'
		epochYr   = 94
		epochDays = 264.51782528
		bTerm     = 0.06822045
		ogParm    = 0.001
		agom      = .0000500000
		elsetNum  = 292
		incli     = 51.6416
		node      = 247.4627
		eccen     = 0.0006703
		omega     = 130.5360
		mnAnomaly = 325.0288
		mnMotion  = 15.72125391
		revNum    = 15390
		satKey    = tledll.TleAddSatFrFieldsSPML(satNum, secClass, satName, epochYr, epochDays, bTerm, ogParm, agom, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum)
		self.assertTrue(satKey.value > 0)
		
	##TleAddSatFrLines
	def test_TleAddSatFrLines(self):
		line1 = '1 23455U 94089A   97320.90946019  .00000140  00000-0  10191-3 0  2621'
		line2 = '2 23455  99.0090 272.6745 0008546 223.1686 136.8816 14.11711747148495'
		satKey = tledll.TleAddSatFrLines(line1, line2)
		self.assertTrue(satKey.value > 0)
	
	##TleAddSatFrLinesML
	@unittest.skip("Segmentation fault, matlab")
	def test_TleAddSatFrLinesML(self):
		line1 = '1 23455U 94089A   97320.90946019  .00000140  00000-0  10191-3 0  2621'
		line2 = '2 23455  99.0090 272.6745 0008546 223.1686 136.8816 14.11711747148495'
		satKey = tledll.TleAddSatFrLinesML(line1, line2)
		self.assertTrue(satKey.value > 0)
		
	##TleDataToArray
	def test_TleDataToArray(self):
		satKey = self.generic_satKey
		(retcode, xa_tle, xs_tle) = tledll.TleDataToArray(satKey)
		pdb.set_trace()
	
	##TleFieldsToSatKey
	##TleFieldsToSatKeyML
	##TleGetAllFieldsGP
	##TleGetAllFieldsGP2
	##TleGetAllFieldsSP
	##TleGetCount
	##TleGetField
	##TleGetInfo
	##TleGetLines
	##TleGetLoaded
	##TleGetSatKey
	##TleGetSatKeyML
	##TleGPArrayToLines
	##TleGPFieldsToLines
	
	##TleInit
	def test_TleInit(self):
		return None #this is effectively tested by the setUp clause
	
	##TleLinesToArray
	def test_TleLinesToArray(self):
		line1 = '1 90004U SGP4-KNW 03 51.03935584  .00001327      0 0  00000-4   882'
		line2 = '2 90004  64.7716 194.9878 6033327 269.3020  18.6110  2.00615358 3847'
		(retcode, xa_tle, xs_tle) = tledll.TleLinesToArray(line1, line2)
		self.assertEqual(retcode, 0)
		
	##TleLoadFile
	##TleParseGP
	##TleParseSP
	##TleRemoveAllSats
	##TleRemoveSat
	##TleSaveFile
	##TleSetField
	##TleSPFieldsToLines
	##TleUpdateSatFrArray
	##TleUpdateSatFrFieldsGP
	##TleUpdateSatFrFieldsGP2
	##TleUpdateSatFrFieldsSP
	
	def tearDown(self):
		tledll.TleRemoveAllSats()
		return None
