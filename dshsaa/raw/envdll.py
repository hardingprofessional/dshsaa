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
	Returns the value representing the shape of the earth being used by the Astro Standards software, either spherical earth or oblate earth 
	
	:return:
		**earth_shape** (*int*) - The value indicates the shape of the earth that is being used in the Astro Standards software: 0=spherical earth, 1= oblate earth
	"""
	earth_shape = C_ENVDLL.EnvGetEarthShape()
	return earth_shape

## EnvGetFkConst
C_ENVDLL.EnvGetFkConst.restype = c.c_double
C_ENVDLL.EnvGetFkConst.argtypes = [c.c_int32]
def EnvGetFkConst(xf_FkCon):
	"""
	Retrieves the value of one of the constants from the current fundamental catalogue (FK) model.
	
	:param:
		**xf_FkCon** (*int*) - An index specifying the constant you wish to retrieve.
 
			========= ==========================================================
			xf_FkCon  Value
			1         C1: Earth rotation rate w.r.t. moving equinox (rad/day)
			2         C1DOT: Earth rotation acceleration (rad/day2)
			3         THGR70: Greenwich angle (1970; rad)
			========= ==========================================================
	
	:return:
		**fkcon** (*float*) - a floating point representation of the requested value	
	"""
	xf_FkCon = c.c_int32(xf_FkCon)
	fkcon = C_ENVDLL.EnvGetFkConst(xf_FkCon)
	return fkcon

## EnvGetFkIdx
C_ENVDLL.EnvGetFkIdx.restype = c.c_int
def EnvGetFkIdx():
	"""
	Returns the current fundamental catalogue (FK) setting. 

	:return:
		**fk_setting** (*int*) - Return the current FK setting as an integer. Valid values are: (4 = FK4, 5 = FK5). The FK model is shared among all the Standardized Astrodynamic Algorithms DLLs in the program. 
	"""
	fk_setting = C_ENVDLL.EnvGetFkIdx()
	return fk_setting

## EnvGetFkPtr
C_ENVDLL.EnvGetFkPtr.restype = settings.stay_int64
def EnvGetFkPtr():
	"""
	Returns a handle that can be used to access the fundamental catalogue (FK) data structure. The handle returned by this function is sometimes called a pointer for historical reasons. The name EnvGetFkPtr comes from the fact that the handle used to be called a pointer. 

	.. note::
		This function is needed when calling the ThetaGrnwch function from TimeFunc.dll. 

	:return:
		**fk_ptr** (*int*) - A handle which can be used to access the FK data structure.

	"""
	fk_ptr = C_ENVDLL.EnvGetFkPtr()
	return fk_ptr

## EnvGetGeoConst
C_ENVDLL.EnvGetGeoConst.restype = c.c_double
C_ENVDLL.EnvGetGeoConst.argtypes = [c.c_int]
def EnvGetGeoConst(xf_GeoCon):
	"""
	Retrieves the value of one of the constants from the current Earth constants (GEO) model. 

	
	:param int xf_GeoCon: An index specifying the constant you wish to retrieve, see XF_GEOCON_? for field specification
		
		+-----------+-----------------------------------------------------------+
		| xf_GeoCon | xf_GeoCon Interpretation                                  |
		+-----------+-----------------------------------------------------------+
		| 1         | FF: Earth flattening (reciprocal; unitless)               |
		+-----------+-----------------------------------------------------------+
		| 2         | J2 (unitless)                                             |
		+-----------+-----------------------------------------------------------+
		| 3         | J3 (unitless)                                             |
		+-----------+-----------------------------------------------------------+
		| 4         | J4 (unitless)                                             |
		+-----------+-----------------------------------------------------------+
		| 5         | KE (er^1.5/min)                                           |
		+-----------+-----------------------------------------------------------+
		| 6         | KMPER: Earth radius (km/er)                               |
		+-----------+-----------------------------------------------------------+
		| 7         | RPTIM: Earth rotation rate w.r.t. fixed equinox (rad/min) |
		+-----------+-----------------------------------------------------------+
		| 8         | CK2: J2/2 (unitless)                                      |
		+-----------+-----------------------------------------------------------+
		| 9         | CK4: -3/8 J4 (unitless)                                   |
		+-----------+-----------------------------------------------------------+
		| 10        | KS2EK: Converts km/sec to er/kem                          |
		+-----------+-----------------------------------------------------------+
		| 11        | THDOT: Earth rotation rate w.r.t. fixed equinox (rad/kem) |
		+-----------+-----------------------------------------------------------+

	:return:
		**geocon** (*float*) - The value of requested value
	"""
	geocon = C_ENVDLL.EnvGetGeoConst(xf_GeoCon)
	return geocon

## EnvGetGeoIdx
C_ENVDLL.EnvGetGeoIdx.restype = c.c_int
def EnvGetGeoIdx():
	"""
	Returns the current Earth constants (GEO) setting. The GEO model is shared among all the Standardized Astrodynamic Algorithms DLLs in the program. 

	:return:
		**geo_idx** (*int*) - The current GEO setting, expressed as an integer.

			+-----+--------------------+
			|value|value interpretation|
			+-----+--------------------+
			| 84  | WGS-84             |
			+-----+--------------------+
			| 96  | EGM-96             |
			+-----+--------------------+
			| 72  | WGS-72 (default)   |
			+-----+--------------------+
			| 2   | JGM2               |
			+-----+--------------------+
			| 68  | STEM68R, SEM68R    |
			+-----+--------------------+
			| 5   | GEM5               |
			+-----+--------------------+
			| 9   | GEM9               |
			+-----+--------------------+
	
	"""
	geo_idx = C_ENVDLL.EnvGetGeoIdx()
	return geo_idx

## EnvGetGeoStr
C_ENVDLL.EnvGetGeoStr.argtypes = [c.c_char_p]
def EnvGetGeoStr():
	"""
	Returns the name of the current Earth constants (GEO) model. 
	
	:return:
		**geo_str** (*str*) - The geoStr parameter may contain one of the following values: 

			+------+
			|WGS-84|
			+------+
			|EGM-96|
			+------+
			|WGS-72|
			+------+
			|JGM2  |
			+------+
			|SEM68R|
			+------+
			|GEM5  |
			+------+
			|GEM9  |
			+------+
	
	"""
	geo_str = c.c_char_p(bytes(6))
	C_ENVDLL.EnvGetGeoStr(geo_str)
	geo_str = settings.byte_to_str(geo_str)
	return geo_str

## EnvGetInfo
C_ENVDLL.EnvGetInfo.argtypes = [c.c_char_p]
def EnvGetInfo():
	"""
	Returns information about the EnvConst DLL. The returned string provides information about the version number, build date, and the platform of the EnvConst DLL. 
	
	:return:
		**info** (*str*) - A string containing information abou the EnvConst DLL
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
	Initializes the EnvInit DLL for use in the program. 
	
	If this function returns an error, it is recommended that you stop the program immediately. 

	An error will occur if you forget to load and initialize all the prerequisite DLLs, as listed in the DLL Prerequisites section of the accompanying documentation, before using this DLL. 

	When the function is called, the GEO model is set to WGS-72 and the FK model is set to FK5. If the user plans to use the SGP4 propagator, DO NOT change this default setting. Otherwise, SGP4 won't work 

	:return:
		**retcode** (*int*) - Returns zero indicating the EnvConst DLL has been initialized successfully. Other values indicate an error.
	"""
	retcode = C_ENVDLL.EnvInit(maindll_handle)
	return retcode

## EnvLoadFile
C_ENVDLL.EnvLoadFile.restype = c.c_int
C_ENVDLL.EnvLoadFile.argtypes = [c.c_char_p]
def EnvLoadFile(envFile):
	"""
	Reads Earth constants (GEO) model and fundamental catalogue (FK) model settings from a file. 

	The users can use NAME=VALUE pair to setup the GEO and FK models in the input file. 

	For GEO model, the valid names are GEOCONST, BCONST and the valid values are WGS-72, WGS72, 72, WGS-84, WGS84, 84, EGM-96, EGM96, 96, JGM-2, JGM2, 2, SEM68R, 68, GEM5, 5, GEM9, and 9. 

	For FK model, the valid name is FKCONST and the valid values are: FK4, 4, FK5, 5. 

	All the string literals are case-insensitive. 

	:return:
		**retcode** (*int*) - Returns zero indicating the input file has been loaded successfully. Other values indicate an error
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
	Saves the current Earth constants (GEO) model and fundamental catalogue (FK) model settings to a file.

	:param str envConstFile: The name of the file in which to save the settings. (string[512])
	:param int saveMode: Specifies whether to create a new file or append to an existing one. (0 = create, 1= append)
	:param int saveForm: Specifies the mode in which to save the file. (0 = text format, 1 = xml (not yet implemented, reserved for future))
	:return: 
		**retcode** (*int*) - Returns zero indicating the GEO and FK settings have been successfully saved to the file. Other values indicate an error.
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
	Specifies the shape of the earth that will be used by the Astro Standards software, either spherical earth or oblate earth 

	:param int earth_shape: The value indicates the shape of the earth: 0=spherical earth, 1= oblate earth (default)
	"""
	earth_shape = c.c_int(earth_shape)
	C_ENVDLL.EnvSetEarthShape(earth_shape)

## EnvSetFkIdx
C_ENVDLL.EnvSetFkIdx.argtypes = [c.c_int]
def EnvSetFkIdx(xf_FkMod):
	"""
	Changes the fundamental catalogue (FK) setting to the specified value. 

	If the users enter an invalid value for the fkIdx, the program will continue to use the current setting.

	The FK model is globally shared among the Standardized Astrodynamic Algorithms DLLs. If its setting is changed, the new setting takes effect immediately.

	The FK model must be set to FK5 to use the SGP4 propagator.
	
	:param int xf_FxKod: Specifies the FK model to use. The following values are accepted: xf_FkMod= 4: FK4, xf_FkMod= 5: FK5
	"""
	if not(xf_FkMod == 4 or xf_FkMod == 5):
		raise Exception("xf_FkMod must be 4 or 5")
	xf_FkMod = c.c_int(xf_FkMod)
	C_ENVDLL.EnvSetFkIdx(xf_FkMod)
	
## EnvSetGeoIdx
C_ENVDLL.EnvSetGeoIdx.argtypes = [c.c_int]
def EnvSetGeoIdx(xf_GeoMod):
	"""
	Changes the Earth constants (GEO) setting to the specified value. 

	:param int xf_GeoMod:

		If you specify an invalid value for xf_GeoMod, the program will continue to use the current setting. 

		The GEO model is globally shared among the Standardized Astrodynamic Algorithms DLLs. If its setting is changed, the new setting takes effect immediately 

		The following table lists possible values of the parameter value GEO setting: 

			+-----+--------------------+
			|value|value interpretation|
			+-----+--------------------+
			| 84  | WGS-84             |
			+-----+--------------------+
			| 96  | EGM-96             |
			+-----+--------------------+
			| 72  | WGS-72 (default)   |
			+-----+--------------------+
			| 2   | JGM2               |
			+-----+--------------------+
			| 68  | STEM68R, SEM68R    |
			+-----+--------------------+
			| 5   | GEM5               |
			+-----+--------------------+
			| 9   | GEM9               |
			+-----+--------------------+
	
	"""
	xf_GeoMod = c.c_int(xf_GeoMod)
	C_ENVDLL.EnvSetGeoIdx(xf_GeoMod)

## EnvSetGeoStr
C_ENVDLL.EnvSetGeoStr.argtypes = [c.c_char_p]
def EnvSetGeoStr(geoStr):
	"""
	Changes the Earth constants (GEO) setting to the model specified by a string literal. 

	:param str geoStr:

		If you specify an invalid value for geoStr, the program will continue to use the current setting. 

		The GEO model is globally shared among the Standardized Astrodynamic Algorithms DLLs. If its setting is changed, the new setting takes effect immediately. 

		The following table lists possible values of the parameter value GEO setting: 

			+--------------------------------+------------------+
			| geoStr (any string in the row) | Interpretation   |
			+--------------------------------+------------------+
			| 'WGS-84', 'WGS84', '84'        | WGS-84           |
			+--------------------------------+------------------+
			| 'EGM-96', 'EGM96', '96'        | EGM-96           |
			+--------------------------------+------------------+
			| 'WGS-72', 'WGS72', '72'        | WGS-72 (default) |
			+--------------------------------+------------------+
			| 'JGM-2, 'JGM2', '2'            | JGM-2            |
			+--------------------------------+------------------+
			| 'SEM68R', '68'                 | STEM68R, SEM68R  |
			+--------------------------------+------------------+
			| 'GEM5', '5'                    | GEM5             |
			+--------------------------------+------------------+
			| 'GEM9', '9'                    | GEM9             |
			+--------------------------------+------------------+

		The GEO model must be set to WGS-72 to use the SGP4 propagator. 


	"""
	geoStr = geoStr.encode('ascii')
	geoStr = settings.enforce_limit(geoStr, 6, terminator = False)
	geoStr = c.c_char_p(geoStr)
	f = C_ENVDLL.EnvSetGeoStr
	C_ENVDLL.EnvSetGeoStr(geoStr)
