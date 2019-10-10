#! /usr/bin/env python3

import dshsaa.raw.settings as settings
import ctypes as c
import pdb

C_ASTRODLL = c.CDLL(settings.LIB_ASTRO_NAME)

##AstroConvFrTo 
C_ASTRODLL.AstroConvFrTo.argtypes = [c.c_int, settings.double128, settings.double128]
def AstroConvFrTo(xf_Conv, frArr, toArr):
	"""
	python:function::AstroConvFrTo
	"""
	xf_Conv = c.c_int(xf_Conv)
	frArr_compatible = settings.double128()
	toArr_compatible = settings.double128()
	frArr_compatible = settings.feed_list_into_array(frArr, frArr_compatible)
	toArr_compatible = settings.feed_list_into_array(toArr, toArr_compatible)
	C_ASTRODLL.AstroConvFrTo(xf_Conv, frArr_compatible, toArr_compatible)

##AstroFuncGetInfo 
##AstroFuncInit
C_ASTRODLL.AstroFuncInit.restype = c.c_int
C_ASTRODLL.AstroFuncInit.argtypes = [settings.stay_int64]
def AstroFuncInit(maindll_handle):
	"""
	python:function::AstroFuncInit
	"""
	retcode = C_ASTRODLL.AstroFuncInit(maindll_handle)
	return retcode

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
 
