#! /usr/bin/env python3

import dshsaa.raw.settings as settings
import ctypes as c
import pdb

C_ENVDLL = c.CDLL(settings.LIB_ENV_NAME)

# The pattern for the rest of this file will be:
# 1. Set parameter types
# 2. Set return types
# 3. Define a python-friendly function

## EnvGetEarthShape
C_ENVDLL.EnvGetEarthShape.restype = c.c_int
def EnvGetEarthShape():
	"""
	python:function:EnvGetEarthShape
	"""
	earth_shape = C_ENVDLL.EnvGetEarthShape()
	return earth_shape

## EnvGetFkConst
C_ENVDLL.EnvGetFkConst.restype = c.c_double
C_ENVDLL.EnvGetFkConst.argtypes = [c.c_int32]
def EnvGetFkConst(xf_FkCon):
	"""
	Retrieves the value of one of the constants from the current fundamental catalogue (FK) model.
	
	========= ==========================================================
	xf_FkCon  Value
	1         C1: Earth rotation rate w.r.t. moving equinox (rad/day)
	2         C1DOT: Earth rotation acceleration (rad/day2)
	3         THGR70: Greenwich angle (1970; rad)
	========= ==========================================================
	
	:param int xf_FkCon: An index specifying the constant you wish to retrieve. See XF_FKCON_? for field specification.
	:return float fkcon: a floating point representation of the requested value	
	"""
	xf_FkCon = c.c_int32(xf_FkCon)
	fkcon = C_ENVDLL.EnvGetFkConst(xf_FkCon)
	return fkcon

## EnvGetFkIdx
C_ENVDLL.EnvGetFkIdx.restype = c.c_int
def EnvGetFkIdx():
	"""
	python:function::EnvGetFkIdx
	"""
	fk_setting = C_ENVDLL.EnvGetFkIdx()
	return fk_setting

## EnvGetFkPtr
C_ENVDLL.EnvGetFkPtr.restype = settings.stay_int64
def EnvGetFkPtr():
	"""
	python:function::EnvGetFkPtr
	"""
	fk_ptr = C_ENVDLL.EnvGetFkPtr()
	return fk_ptr

## EnvGetGeoConst
C_ENVDLL.EnvGetGeoConst.restype = c.c_double
C_ENVDLL.EnvGetGeoConst.argtypes = [c.c_int]
def EnvGetGeoConst(xf_GeoCon):
	"""
	python:function::EnvGetGeoConst
	xf_GeoCon
	xf_GeoCon Interpretation
	1 FF: Earth flattening (reciprocal; unitless)
	2 J2 (unitless)
	3 J3 (unitless)
	4 J4 (unitless)
	5 KE (er^1.5/min)
	6 KMPER: Earth radius (km/er)
	7 RPTIM: Earth rotation rate w.r.t. fixed equinox (rad/min)
	8 CK2: J2/2 (unitless)
	9 CK4: -3/8 J4 (unitless)
	10 KS2EK: Converts km/sec to er/kem
	11 THDOT: Earth rotation rate w.r.t. fixed equinox (rad/kem)
	:param int xf_GeoCon: code for requested value
	:return float geocon: value of requested value
	"""
	geocon = C_ENVDLL.EnvGetGeoConst(xf_GeoCon)
	return geocon

## EnvGetGeoIdx
C_ENVDLL.EnvGetGeoIdx.restype = c.c_int
def EnvGetGeoIdx():
	"""
	python:function::EnvGetGeoIdx
	"""
	geo_idx = C_ENVDLL.EnvGetGeoIdx()
	return geo_idx

## EnvGetGeoStr
C_ENVDLL.EnvGetGeoStr.argtypes = [c.c_char_p]
def EnvGetGeoStr():
	"""
	python:function::EnvGetGeoStr
	"""
	geo_str = c.c_char_p(bytes(6))
	C_ENVDLL.EnvGetGeoStr(geo_str)
	geo_str = settings.byte_to_str(geo_str)
	return geo_str

## EnvGetInfo
C_ENVDLL.EnvGetInfo.argtypes = [c.c_char_p]
def EnvGetInfo():
	"""
	python:function::EnvGetInfo
	"""
	info = c.c_char_p(bytes(128))
	C_ENVDLL.EnvGetInfo(info)
	info = settings.byte_to_str(info)
	return info

## EnvInit
C_ENVDLL.EnvInit.restype = c.c_int
C_ENVDLL.EnvInit.argtypes = [settings.stay_int64]
def EnvInit(maindll_handle):
	"""
	python:function:EnvInit
	"""
	retcode = C_ENVDLL.EnvInit(maindll_handle)
	return retcode

## EnvLoadFile
C_ENVDLL.EnvLoadFile.restype = c.c_int
C_ENVDLL.EnvLoadFile.argtypes = [c.c_char_p]
def EnvLoadFile(envFile):
	"""
	python:function::EnvLoadFile
	"""
	envFile = envFile.encode('ascii')
	envFile = settings.enforce_limit(envFile, 512)
	envFile = c.c_char_p(envFile)
	retcode = C_ENVDLL.EnvLoadFile(envFile)
	return retcode

## EnvSaveFile
C_ENVDLL.EnvSaveFile.restype = c.c_int
C_ENVDLL.EnvSaveFile.artypes = [c.c_char_p, c.c_int, c.c_int]
def EnvSaveFile(envConstFile, saveMode, saveForm):
	"""
	pythong:function::EnvSaveFile
	"""
	envConstFile = envConstFile.encode('ascii')
	envConstFile = settings.enforce_limit(envConstFile, 512)
	envConstFile = c.c_char_p(envConstFile)
	saveMode = c.c_int(saveMode)
	saveForm = c.c_int(saveForm)
	retcode = C_ENVDLL.EnvSaveFile(envConstFile, saveMode, saveForm)
	return retcode

## EnvSetEarthShape
C_ENVDLL.EnvSetEarthShape.argtypes = [c.c_int]
def EnvSetEarthShape(earth_shape):
	"""
	python:function::EnvSetEarthShape
	"""
	earth_shape = c.c_int(earth_shape)
	C_ENVDLL.EnvSetEarthShape(earth_shape)

## EnvSetFkIdx
C_ENVDLL.EnvSetFkIdx.argtypes = [c.c_int]
def EnvSetFkIdx(xf_FkMod):
	"""
	python:function::EnvSetFkIdx
	"""
	xf_FkMod = c.c_int(xf_FkMod)
	C_ENVDLL.EnvSetFkIdx(xf_FkMod)
	
## EnvSetGeoIdx
C_ENVDLL.EnvSetGeoIdx.argtypes = [c.c_int]
def EnvSetGeoIdx(xf_GeoMod):
	"""
	python:function::EnvSetGeoIdx
	"""
	xf_GeoMod = c.c_int(xf_GeoMod)
	C_ENVDLL.EnvSetGeoIdx(xf_GeoMod)

## EnvSetGeoStr
C_ENVDLL.EnvSetGeoStr.argtypes = [c.c_char_p]
def EnvSetGeoStr(geoStr):
	"""
	python:function::EnvSetGeoStr
	"""
	geoStr = geoStr.encode('ascii')
	geoStr = settings.enforce_limit(geoStr, 6, terminator = False)
	geoStr = c.c_char_p(geoStr)
	f = C_ENVDLL.EnvSetGeoStr
	C_ENVDLL.EnvSetGeoStr(geoStr)
