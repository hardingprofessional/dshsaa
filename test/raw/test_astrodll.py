#! /usr/bin/env python3
import unittest
from dshsaa.raw import maindll, envdll, astrodll
from dshsaa.raw import settings
import pdb
import ctypes as c
import os #for cleaning up output files

class TestAstroDLL(unittest.TestCase):
	def setUp(self):
		self.maindll_handle = maindll.DllMainInit()
		self.envdll_retcode = envdll.EnvInit(self.maindll_handle)
		if self.envdll_retcode != 0:
			raise Exception("envdll init retcode was %i != 0" % (self.envdll_retcode))
		self.astrodll_retcode = astrodll.AstroFuncInit(self.maindll_handle)
		if self.astrodll_retcode != 0:
			raise Exception("astrodll init retcode was %i != 0" % (self.astrodll_retcode))
		return None
	##AstroConvFrTo
	def test_AstroConvFrTo(self):
		xf_Conv = 0
		frArr = [0.0]
		toArr = [1.0]
		astrodll.AstroConvFrTo(xf_Conv, frArr, toArr)
		
	##AstroFuncGetInfo 
	##AstroFuncInit
	def test_AstroFuncInit(self):
		# if setUp runs, this is good
		return None
	
	##AToN 
	##AzElToLAD 
	##AzElToRaDec 
	##BrouwerToKozai 
	##ClassToEqnx 
	##CompMoonPos 
	##CompSunMoonPos 
	##CompSunPos 
	##CompTrueAnomaly 
	##CovMtxPTWToUVW 
	##CovMtxUVWToPTW 
	##EarthObstructionAngles 
	##ECIToEFG 
	##ECIToTopoComps 
	##ECRToEFG 
	##EFGPosToLLH 
	##EFGToECI 
	##EFGToECR 
	##EqnxToClass 
	##EqnxToKep 
	##EqnxToPosVel 
	##GetInitialDrag 
	##IsPointSunlit 
	##KepOscToMean 
	##KepToEqnx 
	##KepToPosVel 
	##KepToUVW 
	##KozaiToBrouwer 
	##LLHToEFGPos 
	##LLHToXYZ 
	##NToA 
	##PosVelMuToEqnx 
	##PosVelMuToKep 
	##PosVelToEqnx 
	##PosVelToKep 
	##PosVelToPTW 
	##PosVelToUUVW 
	##RaDecToAzEl 
	##RADecToLAD 
	##RAEToECI 
	##RotDateToJ2K 
	##RotJ2KToDate 
	##SolveKepEqtn 
	##XYZToLLH 
	
	def tearDown(self):
		return None
