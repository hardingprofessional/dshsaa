#! /usr/bin/env python3
import unittest
from dshsaa.raw import maindll, timedll
from dshsaa.raw import settings
import pdb
import ctypes as c
import os #for cleaning up output files

class TestTimeDLL(unittest.TestCase):

	def setUp(self):
		self.maindll_handle = maindll.DllMainInit()
		self.timedll_retcode = timedll.TimeFuncInit(self.maindll_handle)
		if self.timedll_retcode != 0:
			raise Exception("timedll init retcode was %i != 0" % self.timedll_retcode)
		return None

	def test_DTGToUTC(self):
		DTG20 = "2001/123 0304 12.345"
		DTG19 = "2001May03030412.345"
		DTG17 = "2001/123.12792066"
		DTG15 = "01123030412.345"
		utc_dtg20 = timedll.DTGToUTC(DTG20)
		utc_dtg19 = timedll.DTGToUTC(DTG19)
		utc_dtg17 = timedll.DTGToUTC(DTG17)
		utc_dtg15 = timedll.DTGToUTC(DTG15)
		# TODO: Check these values
		self.assertEqual(utc_dtg20, 18751.12792065972)
		self.assertEqual(utc_dtg19, 18751.12792065972)
		self.assertEqual(utc_dtg17, 18751.12792066)
		self.assertEqual(utc_dtg15, 18751.12792065972)

	## Get6P
	@unittest.skip("Need comparison data")
	def test_Get6P(self):
		(startFrEpoch, stopFrEpoch, startTime, stopTime, stepSize) = timedll.Get6P()
		print("\ntest_Get6P Results: \n startFrEpoch = %i\n stopFrEpoch = %i\n startTime = %d\n stopTime = %d\n stepSize = %d\n" % (startFrEpoch, stopFrEpoch, startTime, stopTime, stepSize))
		# self.assertEqual(startFrEpoch, None)
		# self.assertEqual(stopFrEpoch, None)
		# self.assertEqual(startTime, None)
		# self.assertEqual(stopTime, None)
		# self.assertEqual(stepSize, None)

	## Get6PCardLine
	@unittest.skip("Need comparison data")
	def test_Get6PCardLine(self):
		(card6PLine) = timedll.Get6PCardLine()
		self.assertEqual(card6PLine, None)

	## IsTConFileLoaded
	def test_IsTConFileLoaded(self):
		load_status = timedll.IsTConFileLoaded()
		self.assertTrue(load_status != 1)
		# TODO: Load the timing constants and check that IsTConFileLoaded resolves to 1
		
	
	## Set6P
	def test_Set6P(self):
		# Test using values from the documentation
		inp_startFrEpoch = 1
		inp_stopFrEpoch = 1
		inp_startTime = 0
		inp_stopTime = 1440
		inp_stepSize = 360
		timedll.Set6P(inp_startFrEpoch, inp_stopFrEpoch, inp_startTime, inp_stopTime, inp_stepSize)
		(out_startFrEpoch, out_stopFrEpoch, out_startTime, out_stopTime, out_stepSize) = timedll.Get6P()
		self.assertEqual(inp_startFrEpoch, out_startFrEpoch)
		self.assertEqual(inp_stopFrEpoch, out_stopFrEpoch)
		self.assertEqual(inp_startTime, out_startTime)
		self.assertEqual(inp_stopTime, out_stopTime)
		self.assertEqual(inp_stepSize, out_stepSize)
		
		# Test using custom values representing the following:
		# start: 2019-10-01, stop: 2019-10-05, values calculated using timeanddate.com
		inp_startFrEpoch = 0 #start time expressed as days
		inp_stopFrEpoch = 0  #stop time expressed as days
		inp_startTime = 25474#start: 2019-10-01
		inp_stopTime = 25479 #stop: 2019-10-05
		inp_stepSize = 1440  #step size is 1 day (in minutes)
		timedll.Set6P(inp_startFrEpoch, inp_stopFrEpoch, inp_startTime, inp_stopTime, inp_stepSize)
		(out_startFrEpoch, out_stopFrEpoch, out_startTime, out_stopTime, out_stepSize) = timedll.Get6P()
		self.assertEqual(inp_startFrEpoch, out_startFrEpoch)
		self.assertEqual(inp_stopFrEpoch, out_stopFrEpoch)
		self.assertEqual(inp_startTime, out_startTime)
		self.assertEqual(inp_stopTime, out_stopTime)
		self.assertEqual(inp_stepSize, out_stepSize)		
		
	## TAIToUT1
	def test_TAIToUT1(self):
		ds50TAI = 1450.6
		ds50UT1 = timedll.TAIToUT1(ds50TAI)
		# TODO: Add test case where we load timing constants
		self.assertEqual(ds50TAI, ds50UT1)
		
	## TAIToUTC
	def test_TAIToUTC(self):
		ds50TAI = 1450.6
		ds50UTC = timedll.TAIToUTC(ds50TAI)
		# TODO: Add test case where we load timing constants
		self.assertEqual(ds50TAI, ds50UTC)
	
	@unittest.skip("Error, need to investigate, compare to TConAddOne")
	## TConAddARec
	def test_TConAddARec(self):
		refDs50UTC  = 0.0
		leapDs50UTC = 0.0
		taiMinusUTC = 0.0
		ut1MinusUTC = 0.0
		ut1Rate     = 0.0
		polarX      = 0.0
		polarY      = 0.0
		retcode = timedll.TConAddARec(refDs50UTC, leapDs50UTC, taiMinusUTC, ut1MinusUTC, ut1Rate, polarX, polarY)
		#TODO: Find a time constants file and copy values into the above test
		#TODO: Figure out why the above dataset results in an error code
		self.assertEqual(retcode, 0)
		
	## TConAddOne
	#
	def test_TConAddOne(self):
		refDs50UTC  = 0.0
		leapDs50UTC = 0.0
		taiMinusUTC = 0.0
		ut1MinusUTC = 0.0
		ut1Rate     = 0.0
		polarX      = 0.0
		polarY      = 0.0
		retcode = timedll.TConAddOne(refDs50UTC, leapDs50UTC, taiMinusUTC, ut1MinusUTC, ut1Rate, polarX, polarY)
		#TODO: Find a time constants file and copy values into the above test
		self.assertEqual(retcode, 0)
	
	## TConLoadFile
	@unittest.skip("Need real time constant data")
	def test_TConLoadFile(self):
		retcode = timedll.TConLoadFile("TimeConstants.txt")
		self.assertEqual(retcode, 0)
	
	## TConRemoveAll
	def test_TConRemoveAll(self):
		retcode = timedll.TConRemoveAll()
		self.assertEqual(retcode, 0)	
	
	## TConSaveFile
	def test_TConSaveFile(self):
		tconfile = "test_TConSaveFile_TimeConstants.txt"
		saveMode = 0
		saveForm = 0
		retcode = timedll.TConSaveFile(tconfile, saveMode, saveForm)
		self.assertEqual(retcode, 0)
		os.remove(tconfile)
		#TODO: Load time constants into memory, sae them with this function, then check the file
	
	## ThetaGrnwch
	@unittest.skip("Must implement envdll.EnvGetFkPtr() to run this test")
	def test_ThetaGrnwch(self):
		ds50UT1 = 30
		envFk = envdll.EnvGetFkPtr()
		thetaGrnwhch = timedll.ThetaGrnwch(ds50UT1, envFk)
		# TODO: Come up with a trusted test value for test_ThetaGrnwch
		self.assertIsInstance(thetaGrnwch, float)
	
	## ThetaGrnwchFK4
	def test_ThetaGrnwchFK4(self):
		ds50UT1 = 46
		theta = timedll.ThetaGrnwchFK4(ds50UT1)
		# TODO: Come up with a trusted test value for test_ThetaGrnwchFK4
		self.assertIsInstance(theta, float)	
	
	## ThetaGrnwchFK5
	def test_ThetaGrnwchFK5(self):
		ds50UT1 = 46
		theta = timedll.ThetaGrnwchFK5(ds50UT1)
		# TODO: Come up with a trusted test value for test_ThetaGrnwchFK5
		self.assertIsInstance(theta, float)	
	
	## TimeComps1ToUTC
	def test_TimeComps1ToUTC(self):
		year = 3
		dayOfYear = 123
		hh = 12
		mm = 13
		sss = 14.567
		ds50UTC = timedll.TimeComps1ToUTC(year, dayOfYear, hh, mm, sss)
		# TODO: Come up with a trusted test value for test_TimeComps1ToUTC
		self.assertIsInstance(ds50UTC, float)
	
	## TimeComps2ToUTC
	def test_TimeComps2ToUTC(self):
		year = 3
		month = 4
		dayOfMonth = 12
		hh = 12
		mm = 13
		sss = 14.567
		ds50UTC = timedll.TimeComps2ToUTC(year, month, dayOfMonth, hh, mm, sss)
		# TODO: Come up with a trusted test value for test_TimeComps2ToUTC
		self.assertIsInstance(ds50UTC, float)
	
	## TimeConvFrTo
	def test_TimeConvFrTo(self):
		funcIdx = 0
		frArr = [0.0]
		toArr = [1.0]
		timedll.TimeConvFrTo(funcIdx, frArr, toArr)
		#TODO: when AFSPC tells us what this does, come up with a better test
	
	## TimeFuncGetInfo
	def test_TimeFuncGetInfo(self):
		infoStr = timedll.TimeFuncGetInfo()
	
	## TimeFuncInit
	def test_TimeFuncInit(self):
		# time function is init'd during the setup phase
		1
	
	## TimeFuncLoadFile
	def test_TimeFuncLoadFile(self):
		retcode = timedll.TimeFuncLoadFile("test/raw/test_TimeFuncLoadFile_tconfile.txt")
		self.assertEqual(retcode, 0)

	## UTCToDTG15
	def test_UTCToDTG15(self):
		ds50UTC = 18751.12792065972
		dtg15 = timedll.UTCToDTG15(ds50UTC)
		self.assertEqual(dtg15, "01123030412.345")

	## UTCToDTG17
	def test_UTCToDTG17(self):
		ds50UTC = 18751.12792066
		dtg17 = timedll.UTCToDTG17(ds50UTC)
		self.assertEqual(dtg17, "2001/123.12792066")

	## UTCToDTG19
	@unittest.skip("DLL core dumps")
	def test_UTCToDTG19(self):
		ds50UTC = 18751.12792065972
		# Something about ds50UTC is causing the underlying function to core with no log messages
		maindll.OpenLogFile('2019-10-01.log')
		dtg19 = timedll.UTCToDTG19(ds50UTC)
		self.assertEqual(dtg19, "2001May03030412.345")

	## UTCToDTG20
	def test_UTCToDTG15(self):
		ds50UTC = 18751.12792065972
		dtg20 = timedll.UTCToDTG20(ds50UTC)
		self.assertEqual(dtg20, "2001/123 0304 12.345")

	## UTCToET
	## UTCToTAI
	## UTCToConRec
	## UTCToTimeComps1
	## UTCToTimeComps2
	## UTCToUT1
	## UTCToYrDays
	## YrDaysToUTC





	def tearDown(self):
		return None




if __name__ == '__main__':
	unittest.main()
