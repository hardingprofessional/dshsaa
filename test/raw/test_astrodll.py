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
		toArr = astrodll.AstroConvFrTo(xf_Conv, frArr)
		
	##AstroFuncGetInfo
	def test_AstroFuncGetInfo(self):
		infoStr = astrodll.AstroFuncGetInfo()
		self.assertIsInstance(infoStr, str)
		
	##AstroFuncInit
	def test_AstroFuncInit(self):
		# if setUp runs, this is good
		return None
	
	##AToN
	def test_AToN(self):
		a =  1.496e+08
		N = astrodll.AToN(a)
		
	##AzElToLAD
	def test_AzElToLAD(self):
		az = 20
		el = 30
		(Lh, Ah, Dh) = astrodll.AzElToLAD(az, el)

	##AzElToRaDec
	def test_AzElToRaDec(self):
		thetaG = 3.14
		lat = 20
		lon = 100
		az = 30
		el = 45
		(RA, dec) = astrodll.AzElToRaDec(thetaG, lat, lon, az, el)
		
	##BrouwerToKozai 
	def test_BrouwerToKozai(self):
		eccen = 0.9
		incli = 30
		nBrouwer = .8
		kozai = astrodll.BrouwerToKozai(eccen, incli, nBrouwer)

	##ClassToEqnx
	@unittest.skip("don't know sequence of classical elements in metricClass")
	def test_ClassToEqnx(self):
		metricClass = [1,1,1,1,1,1]

	##CompMoonPos
	def test_CompMoonPos(self):
		ds50ET = 18751.12792066
		(uvecMoon, moonVecMag) = astrodll.CompMoonPos(ds50ET)


	##CompSunMoonPos 
	def test_CompSunMoonPos(self):
		ds50ET = 18751.12792066
		(uvecSun, sunVecMag, uvecMoon, moonVecMag) = astrodll.CompSunMoonPos(ds50ET)
		# TODO: calculate appropriate test values
		
	##CompSunPos 
	def test_CompSunPos(self):
		ds50ET = 18751.12792066
		(uvecSun, sunVecMag) = astrodll.CompSunPos(ds50ET)
		# TODO: caluclate appropriate test values

	##CompTrueAnomaly
	def test_CompTrueAnomaly(self):
		metricKep = [42165.91800738855, 5.436305581337673e-05, 0.0344453177014498, 101.51166906837908, 157.12250758872392, 101.37732368917199]
		true_anomaly = astrodll.CompTrueAnomaly(metricKep)
	
	##CovMtxPTWToUVW
	def test_CovMtxPTWToUVW(self):
		#TODO: Find better numbers
		pos = [1,1,1]
		vel = [1,1,1]
		ptwCovMtx = [[.1 for i in range(6)] for j in range(6)]
		uvwCovMtx = astrodll.CovMtxPTWToUVW(pos, vel, ptwCovMtx)
	
	##CovMtxUVWToPTW 
	def test_CovMtxUVWToPTW(self):
		#TODO: Find better numbers
		pos = [1,1,1]
		vel = [1,1,1]
		uvwCovMtx = [[.1 for i in range(6)] for j in range(6)]
		ptwCovMtx = astrodll.CovMtxPTWToUVW(pos, vel, uvwCovMtx)
		
	##EarthObstructionAngles
	def test_EarthObstructionAngles(self):
		#TODO: Find Better Numbers
		earthLimb = 100
		satECI = [7000, 600, 0]
		senECI = [7000, -600, 0]
		(earthSenLimb, earthSenSat, satEarthSen) = astrodll.EarthObstructionAngles(earthLimb, satECI, senECI)
		
	##ECIToEFG 
	def test_ECIToEFG(self):
		thetaG = 0.1
		posECI = [7000, 100, 100]
		velECI = [100, 1000, -100]
		(posEFG, velEFG) = astrodll.ECIToEFG(thetaG, posECI, velECI)
		# TODO: write some valid test examples
		
	##ECIToTopoComps
	def test_ECIToTopoComps(self):
		theta = 0.1
		lat = 20.3
		senPos = [6500, 75, 50]
		satPos = [7000, 100, 200]
		satVel = [0, 2000, 0]
		xa_topo = astrodll.ECIToTopoComps(theta, lat, senPos, satPos, satVel)

	##ECRToEFG 
	def test_ECRToEFG(self):
		polarX = 1
		polarY = 1
		posECR = [7000, 100, 100]
		velECR = [100, 2000, 100]
		(posEFG, velEFG) = astrodll.ECRToEFG(polarX, polarY, posECR, velECR)

	##EFGPosToLLH
	def test_EFGPosToLLH(self):
		posEFG = [7000, 100, 100]
		metricLLH = astrodll.EFGPosToLLH(posEFG)
		
	##EFGToECI
	def test_EFGToECI(self):
		posEFG = [7000, 100, 100]
		velEFG = [100, 2000, 100]
		thetaG = 0.3
		(posECI, velECI) = astrodll.EFGToECI(thetaG, posEFG, velEFG)
		
	##EFGToECR 
	def test_EFGToECR(self):
		posEFG = [7000, 100, 100]
		velEFG = [100, 2000, 100]
		polarX = 0.1
		polarY = 0.1
		(posECR, velECR) = astrodll.EFGToECR(polarX, polarY, posEFG, velEFG)
		
	##EqnxToClass
	def test_EqnxToClass(self):
		# This test data is the output of test_PosVelToEqnx
		metricEqnx = [-1.0838407018247723e-05, 
					  -5.327166949397317e-05, 
					   0.00011685880548969324, 
					  -0.0002769469937440215, 
					   0.01150034627496683, 
					   1.0026759940340393]
		metricClass = astrodll.EqnxToClass(metricEqnx)
		
	##EqnxToKep 
	def test_EqnxToKep(self):
		# This test data is the output of test_PosVelToEqnx
		metricEqnx = [-1.0838407018247723e-05, 
					  -5.327166949397317e-05, 
					   0.00011685880548969324, 
					  -0.0002769469937440215, 
					   0.01150034627496683, 
					   1.0026759940340393]
		metricKep = astrodll.EqnxToKep(metricEqnx)
	
	##EqnxToPosVel
	def test_EqnxToPosVel(self):
		# This test data is the output of test_PosVelToEqnx
		metricEqnx = [-1.0838407018247723e-05, 
					  -5.327166949397317e-05, 
					   0.00011685880548969324, 
					  -0.0002769469937440215, 
					   0.01150034627496683, 
					   1.0026759940340393]
		(pos, vel) = astrodll.EqnxToPosVel(metricEqnx)
	
	##GetInitialDrag
	def test_GetInitialDrag(self):
		semiMajorAxis = 10000
		eccen = 0.5
		(ndot, bstar) = astrodll.GetInitialDrag(semiMajorAxis, eccen)
		# TODO: The output data from this doesn't give me warm feelies
		
	##IsPointSunlit 
	@unittest.skip("Investigate why point is always sunlit")
	def test_IsPointSunlit(self):
		# actual ISS position when I wrote this
		ptEci = [-2001.7, 3696.3, 5332.3]		
		# generate 25 hours of ds50ET timestamps
		delta = [h/24 for h in range(0,25,1)]
		ds50ET_r = [18751.12792066 + d for d in delta]
		# determine sunlit status
		sunlit_r = [astrodll.IsPointSunlit(ds50ET, ptEci) for ds50ET in ds50ET_r]
		# TODO: Function does not work correctly. Always returns true. Investigate.
		
	##KepOscToMean
	def test_KepOscToMean(self):
		metricOscKep = [42165.9171734, 0.0000544, 0.0344449, 157.1221806, 101.3605481, 101.5348757]
		metricMeanKep = astrodll.KepOscToMean(metricOscKep)
		
	##KepToEqnx
	def test_KepToEqnx(self):
		metricKep = [42165.91800738855, 5.436305581337673e-05, 0.0344453177014498, 101.51166906837908, 157.12250758872392, 101.37732368917199]
		metricEqnx = astrodll.KepToEqnx(metricKep)
		
	##KepToPosVel
	def test_KepToPosVel(self):
		metricKep = [42165.91800738855, 5.436305581337673e-05, 0.0344453177014498, 101.51166906837908, 157.12250758872392, 101.37732368917199]
		(pos, vel) = astrodll.KepToPosVel(metricKep)
	
	##KepToUVW
	def test_KepToUVW(self):
		metricKep = [42165.91800738855, 5.436305581337673e-05, 0.0344453177014498, 101.51166906837908, 157.12250758872392, 101.37732368917199]
		(uBar, vBar, wBar) = astrodll.KepToUVW(metricKep)
		
	##KozaiToBrouwer
	def test_KozaiToBrouwer(self):
		eccen = 0.1
		incli = 30
		nKozai = 0.9
		nBrouwer = astrodll.KozaiToBrouwer(eccen, incli, nKozai)
	
	##LLHToEFGPos
	def test_LLHToEFGPos(self):
		metricLLH = [30, 30, 100]
		posEFG = astrodll.LLHToEFGPos(metricLLH)
		
	##LLHToXYZ
	def test_LLHToXYZ(self):
		thetaG = 0.1
		metricLLH = [30, 30, 100]
		metricXYZ = astrodll.LLHToXYZ(thetaG, metricLLH)
	
	##NToA
	def test_NToA(self):
		n = 15.50271819 #ISS on 2019-11-07T09:45:00 EDT
		a = astrodll.NToA(n)
	
	##PosVelMuToEqnx
	def test_PosVelMuToEqnx(self):
		pos = [42166.3724464, 12.9531593, -9.8621994]
		vel = [-0.0007811, 3.0745638, -0.0017028]
		mu = 3.986e5 #I'm guessing this is the gravitational parameter of earth in km^3/s^2
		metricEqnx = astrodll.PosVelMuToEqnx(pos, vel, mu)
	
	##PosVelMuToKep
	def test_PosVelMuToKep(self):
		pos = [42166.3724464, 12.9531593, -9.8621994]
		vel = [-0.0007811, 3.0745638, -0.0017028]
		mu = 3.986e5 #I'm guessing this is the gravitational parameter of earth in km^3/s^2
		metricKep = astrodll.PosVelMuToKep(pos, vel, mu)
		
	##PosVelToEqnx
	def test_PosVelToEqnx(self):
		# This is known valid test data taken from the official validation package
		pos = [42166.3724464, 12.9531593, -9.8621994]
		vel = [-0.0007811, 3.0745638, -0.0017028]
		metricEqnx = astrodll.PosVelToEqnx(pos, vel)
		
	##PosVelToKep
	def test_PosVelToKep(self):
		pos = [42166.3724464, 12.9531593, -9.8621994]
		vel = [-0.0007811, 3.0745638, -0.0017028]
		metricKep = astrodll.PosVelToKep(pos, vel)
		
	##PosVelToPTW
	def test_PosVelToPTW(self):
		pos = [42166.3724464, 12.9531593, -9.8621994]
		vel = [-0.0007811, 3.0745638, -0.0017028]
		(uVec, vVec, wVec) = astrodll.PosVelToPTW(pos, vel)
		
	##PosVelToUUVW
	def test_PosVelToUUVW(self):
		pos = [42166.3724464, 12.9531593, -9.8621994]
		vel = [-0.0007811, 3.0745638, -0.0017028]
		(uVec, vVec, wVec) = astrodll.PosVelToUUVW(pos, vel)
		
	##RaDecToAzEl
	def test_RaDecToAzEl(self):
		thetaG = 0.1
		lat = 30
		lon = 30
		RA = 20
		dec = 25
		(az, el) = astrodll.RaDecToAzEl(thetaG, lat, lon, RA, dec)
	
	##RADecToLAD
	def test_RADecToLAD(self):
		RA = 20
		dec = 25
		(L, A_Tilde, D_Tilde) = astrodll.RADecToLAD(RA, dec)
		
	##RAEToECI
	@unittest.skip("Investigate why sensor position is origin (probably need better test data)")
	def test_RAEToECI(self):
		theta = 0.1
		astroLat = 30
		xa_rae = [3000, 30, 50, 230, 1.3, 0.2]
		(senPos, satPos, satVel) = astrodll.RAEToECI(theta, astroLat, xa_rae)
		
	##RotDateToJ2K
	def test_RotDateToJ2K(self):
		spectr = 0
		nutationTerms = 4
		ds50TAI = 1450.6
		posDate = [42166.3724464, 12.9531593, -9.8621994]
		velDate = [-0.0007811, 3.0745638, -0.0017028]
		(posJ2K, velJ2K) = astrodll.RotDateToJ2K(spectr, nutationTerms, ds50TAI, posDate, velDate)
		
		spectr = 1
		nutationTerms = 106
		ds50TAI = 1450.6
		posDate = [42166.3724464, 12.9531593, -9.8621994]
		velDate = [-0.0007811, 3.0745638, -0.0017028]
		(posJ2K, velJ2K) = astrodll.RotDateToJ2K(spectr, nutationTerms, ds50TAI, posDate, velDate)
		
	##RotJ2KToDate
	def test_RotJ2KToDate(self):
		spectr = 1
		nutationTerms = 106
		ds50TAI = 1450.6
		posJ2K = [42163.6334483918, 446.917077357031, 177.51025732759814]
		velJ2K = [-0.03241581573330085, 3.0743929400078627, -0.0018262627529628522]
		spectr = 0
		nutationTerms = 4
		ds50TAI = 1450.6
		posJ2K = [42163.6334483918, 446.917077357031, 177.51025732759814]
		velJ2K = [-0.03241581573330085, 3.0743929400078627, -0.0018262627529628522]
		
	##SolveKepEqtn
	def test_SolveKepEqtn(self):
		metricKep = [42165.91800738855, 5.436305581337673e-05, 0.0344453177014498, 101.51166906837908, 157.12250758872392, 101.37732368917199]
		E = astrodll.SolveKepEqtn(metricKep)
		
	##XYZToLLH
	def test_XYZToLLH(self):
		thetaG = 0.1
		metricPos = [42166.3724464, 12.9531593, -9.8621994]
		metricLLH = astrodll.XYZToLLH(thetaG, metricPos)
	
	def tearDown(self):
		return None
