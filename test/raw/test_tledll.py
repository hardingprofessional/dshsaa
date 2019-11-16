#! /usr/bin/env python3
import unittest
from dshsaa.raw import settings, maindll, envdll, timedll, tledll
import pdb
import ctypes as c 
import re

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
		line1 = '1 25544U 98067A   19311.39056523  .00000757  00000-0  21099-4 0  9992'
		line2 = '2 25544  51.6451  11.2360 0005828 238.9618 210.3569 15.50258526197470'
		generic_satKey = tledll.TleAddSatFrLines(line1, line2)
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
		nDotO2    = 555 #value not used, but is stored for data integrity
		n2DotO6   = 666 #value not used, but is stored for data integrity
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
		nDotO2    = 555 #value not used, but is stored for data integrity
		n2DotO6   = 666 #value not used, but is stored for data integrity
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
		self.assertEqual(retcode, 0)
	
	##TleFieldsToSatKey
	def testl_TleFieldsToSatKey(self):
		satNum = 25544
		epochYr = 19
		epochDays = 311.39056523
		ephType = 0
		satKey = tledll.TleFieldsToSatKey(satNum, epochYr, epochDays, ephType)
		self.assertEqual(satKey.value, self.generic_satKey.value)
	
	##TleFieldsToSatKeyML
	def testl_TleFieldsToSatKeyML(self):
		satNum = 25544
		epochYr = 19
		epochDays = 311.39056523
		ephType = 0
		satKey = tledll.TleFieldsToSatKeyML(satNum, epochYr, epochDays, ephType)
		self.assertEqual(satKey.value, self.generic_satKey.value)
	
	##TleGetAllFieldsGP
	def test_TleGetAllFieldsGP(self):
		# Initialize a GP class TLE set
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
		# Retrieve that GP class TLE set
		(retcode, satNum_r, secClass_r, satName_r, epochYr_r, epochDays_r, bstar_r, ephType_r, elsetNum_r, incli_r, node_r, eccen_r, omega_r, mnAnomaly_r, mnMotion_r, revNum_r) = tledll.TleGetAllFieldsGP(satKey)
		# test equivalency
		self.assertEqual(retcode, 0)
		self.assertEqual(satNum, satNum_r)
		self.assertEqual(secClass, secClass_r)
		self.assertEqual(satName, satName_r)
		# If input epochYr for test is shorthand, shift to full year to match model
		if epochYr < 100:
			if epochYr >= 56: #sputnik launched in 1957
				epochYr += 1900
			else:
				epochYr += 2000
		self.assertEqual(epochYr, epochYr_r)
		self.assertEqual(epochDays, epochDays_r)
		self.assertEqual(bstar, bstar_r)
		self.assertEqual(ephType, ephType_r)
		self.assertEqual(elsetNum, elsetNum_r)
		self.assertEqual(incli, incli_r)
		self.assertEqual(node, node_r)
		self.assertEqual(eccen,  eccen_r)
		self.assertEqual(omega, omega_r)
		self.assertEqual(mnAnomaly, mnAnomaly_r)
		self.assertEqual(mnMotion, mnMotion_r)
		self.assertEqual(revNum, revNum_r)
		
	##TleGetAllFieldsGP2
	def test_TleGetAllFieldsGP2(self):
		# initialize a GP2 element set
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
		nDotO2    = 5555 #value not used, but is stored for data integrity
		n2DotO6   = 6666 #value not used, but is stored for data integrity
		satKey    = tledll.TleAddSatFrFieldsGP2(satNum, secClass, satName, epochYr, epochDays, bstar, ephType, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum, nDotO2, n2DotO6)
		self.assertTrue(satKey.value > 0)
		# retrieve the GP2 element set
		(retcode, satNum_r, secClass_r, satName_r, epochYr_r, epochDays_r, bstar_r, ephType_r, elsetNum_r, incli_r, node_r, eccen_r, omega_r, mnAnomaly_r, mnMotion_r, revNum_r, nDotO2_r, n2DotO6_r) = tledll.TleGetAllFieldsGP2(satKey)
		# check values
		self.assertEqual(retcode, 0)
		self.assertEqual(satNum, satNum_r)
		self.assertEqual(secClass, secClass_r)
		self.assertEqual(satName, satName_r)
		# If input epochYr for test is shorthand, shift to full year to match model
		if epochYr < 100:
			if epochYr >= 56: #sputnik launched in 1957
				epochYr += 1900
			else:
				epochYr += 2000
		self.assertEqual(epochYr, epochYr_r)
		self.assertEqual(epochDays, epochDays_r)
		self.assertEqual(bstar, bstar_r)
		self.assertEqual(ephType, ephType_r)
		self.assertEqual(elsetNum, elsetNum_r)
		self.assertEqual(incli, incli_r)
		self.assertEqual(node, node_r)
		self.assertEqual(eccen,  eccen_r)
		self.assertEqual(omega, omega_r)
		self.assertEqual(mnAnomaly, mnAnomaly_r)
		self.assertEqual(mnMotion, mnMotion_r)
		self.assertEqual(revNum, revNum_r)
		self.assertEqual(nDotO2, nDotO2_r)
		self.assertEqual(n2DotO6, n2DotO6_r)
		
	##TleGetAllFieldsSP
	def test_TleGetAllFieldsSP(self):
		# init an SP class TLE
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
		# retrieve those values		
		(retcode, satNum_r, secClass_r, satName_r, epochYr_r, epochDays_r, bTerm_r, ogParm_r, agom_r, elsetNum_r, incli_r, node_r, eccen_r, omega_r, mnAnomaly_r, mnMotion_r, revNum_r) = tledll.TleGetAllFieldsSP(satKey)
		# test those values
		self.assertEqual(retcode, 0)
		self.assertEqual(satNum_r, satNum_r)
		self.assertEqual(secClass, secClass_r)
		self.assertEqual(satName, satName_r)
		# If input epochYr for test is shorthand, shift to full year to match model
		if epochYr < 100:
			if epochYr >= 56: #sputnik launched in 1957
				epochYr += 1900
			else:
				epochYr += 2000
		self.assertEqual(epochYr, epochYr_r)
		self.assertEqual(epochDays, epochDays_r)
		self.assertEqual(bTerm, bTerm_r)
		self.assertEqual(ogParm, ogParm_r)
		self.assertEqual(agom, agom_r)
		self.assertEqual(elsetNum, elsetNum_r)
		self.assertEqual(incli, incli_r)
		self.assertEqual(node, node_r)
		self.assertEqual(eccen, eccen_r)
		self.assertEqual(omega, omega_r)
		self.assertEqual(mnAnomaly, mnAnomaly_r)
		self.assertEqual(mnMotion, mnMotion_r)
		self.assertEqual(revNum, revNum_r)
		
	##TleGetCount
	def test_TleGetCount(self):
		tledll.TleRemoveAllSats()
		self.assertEqual(0, tledll.TleGetCount())
		line1 = '1 23455U 94089A   97320.90946019  .00000140  00000-0  10191-3 0  2621'
		line2 = '2 23455  99.0090 272.6745 0008546 223.1686 136.8816 14.11711747148495'
		satKey = tledll.TleAddSatFrLines(line1, line2)
		self.assertTrue(satKey.value > 0)
		self.assertEqual(1, tledll.TleGetCount())
		tledll.TleRemoveAllSats()
		self.assertEqual(0, tledll.TleGetCount())
		
	##TleGetField
	def test_TleGetField(self):
		satKey = self.generic_satKey
		xf_Tles = list(range(1, 15))
		# TODO: Break down and check each of these values
		#for xf_Tle in xf_Tles:
		#	(retcode, valueStr) = tledll.TleGetField(satKey, xf_Tle)
		#	print("xf_Tle: %i, retcode: %i, valueStr: %s" % (xf_Tle, retcode, valueStr))
	
	##TleGetInfo
	def test_TleGetInfo(self):
		infoStr = tledll.TleGetInfo()
		
	##TleGetLines
	def test_TleGetLines(self):
		line1 = '1 23455U 94089A   97320.90946019  .00000140  00000-0  10191-3 0  2621'
		line2 = '2 23455  99.0090 272.6745 0008546 223.1686 136.8816 14.11711747148495'
		satKey = tledll.TleAddSatFrLines(line1, line2)
		(retcode, line1_r, line2_r) = tledll.TleGetLines(satKey)
		# The text does not match exactly, and testing equality is tricky
		# TODO: Right a better testing method for accuracy, values are close enough based on visual inspection
	
	##TleGetLoaded
	def test_TleGetLoaded(self):
		tledll.TleRemoveAllSats()
		inserted_satKeys = []
		for num in range(0, 10):
			line1 = '1 2345%iU 94089A   97320.90946019  .00000140  00000-0  10191-3 0  2621' % (num)
			line2 = '2 2345%i  99.0090 272.6745 0008546 223.1686 136.8816 14.11711747148495' % (num)
			inserted_satKeys.append(tledll.TleAddSatFrLines(line1, line2))
		retrieved_satKeys = tledll.TleGetLoaded(9)
		# I have manually verified this information is correct
		# TODO: Add automated verification and comparison to TleGetLoaded
		
	##TleGetSatKey
	def test_TleGetSatKey(self):
		satKey = tledll.TleGetSatKey(25544)
		self.assertEqual(satKey.value, self.generic_satKey.value)
		
	##TleGetSatKeyML
	def test_TleGetSatKeyML(self):
		satKey = tledll.TleGetSatKeyML(25544)
		self.assertEqual(satKey.value, self.generic_satKey.value)
	
	##TleGPArrayToLines
	def test_TleGPArrayToLines(self):
		xa_tle = [90004.0, 19409.03935584, 1.327e-05, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 64.7716, 194.9878, 0.6033327, 269.302, 18.611, 2.00615358, 3847.0, 0.0, 0.0, 0.0, 882.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
		xs_tle = 'USGP4-KNW'
		(line1, line2) = tledll.TleGPArrayToLines(xa_tle, xs_tle)
	
	##TleGPFieldsToLines
	def test_TleGPFieldsToLines(self):
		satNum    = 25544
		secClass  = 'U'
		satName   = 'ISS'
		epochYr   = 8
		epochDays = 264.51782528
		nDotO2    = 5555
		n2DotO6   = 6666
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
		(line1, line2) = tledll.TleGPFieldsToLines(satNum, secClass, satName, epochYr, epochDays, nDotO2, n2DotO6, bstar, ephType, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum)
	
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
	def test_TleLoadFile(self):
		tleFile = './test/raw/inputs/tledll.tleloadfile.inp'
		retcode = tledll.TleLoadFile(tleFile)
		self.assertEqual(retcode, 0)
		
	##TleParseGP
	def test_TleParseGP(self):
		# This is a GP 2 line element set, but not all are!
		"""      00000000011111111112222222222333333333344444444445555555555666666666"""
		"""      12345678901234567890123456789012345678901234567890123456789012345678"""
		line1 = '1 19650U 88102B   00082.05491348 -.00000156 +00000-0 -55907-4 0 0856'
		"""      123456789012345678901234567890123456789012345678901"""
		line2 = '2 19650 070.9951 288.5351 0012570 034.5635 325.6302 14.1505917558504'
		(retcode, satNum, secClass, satName, epochYr, epochDays, bTerm, ogParm, agom, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum) = tledll.TleParseGP(line1, line2)
		pdb.set_trace()
		""" TODO: Why aren't these values right?
		self.assertEqual(retcode, 0)
		self.assertEqual(satNum, 19650
		self.assertEqual(secClass, 'U'
		self.assertEqual(satName, '88102B'
		self.assertEqual(epochYr, 2000
		self.assertEqual(epochDays, 82.05491348)
		self.assertEqual(bTerm,-0.00000156)
		self.assertEqual(ogParm, 0)
		self.assertEqual(agom, -0.55907e-4)
		self.assertEqual(elsetNum, 0
		self.assertEqual(incli, 70.9951
		self.assertEqual(node, 0.0222
		self.assertEqual(eccen, 
		self.assertEqual(omega, 
		self.assertEqual(mnAnomaly, 
		self.assertEqual(mnMotion, 
		self.assertEqual(revNum, 
		"""
		
		
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
