#! /usr/bin/env python3
from dshsaa.raw import settings, exceptions
import ctypes as c
import pdb

C_SGP4DLL = c.CDLL(settings.LIB_SGP4_NAME)

##Sgp4GetInfo 
C_SGP4DLL.Sgp4GetInfo.argtypes = [c.c_char_p]

def Sgp4GetInfo():
	"""
	python:function::Sgp4GetInfo
	Returns information about the current version of Sgp4Prop.dll.
	:retrun str infoStr: A string containing information about Sgp4
	"""
	infoStr = c.c_char_p(bytes(128))
	C_SGP4DLL.Sgp4GetInfo(infoStr)
	infoStr = settings.byte_to_str(infoStr)
	return infoStr

##Sgp4GetLicFilePath
C_SGP4DLL.Sgp4GetLicFilePath.argtypes = [c.c_char_p]

def Sgp4GetLicFilePath():
	"""
	:python:function::Sgp4GetLicFilePath
	Returns the current path to the Sgp4 Open License File
	:return str LicFilePath: The path to the current license file
	"""
	licFilePath = c.c_char_p(bytes(512))
	C_SGP4DLL.Sgp4GetLicFilePath(licFilePath)
	licFilePath = settings.byte_to_str(licFilePath)
	return licFilePath

##Sgp4GetPropOut
C_SGP4DLL.Sgp4GetPropOut.restype = c.c_int
# argument types defined within the function
def Sgp4GetPropOut(satKey, xf_Sgp4Out):
	"""
	python:function::Sgp4GetPropOut
	Retrieves propagator's precomputed results. This function can be used to obtain results from a propagation which are not made available through calls to the propagation functions themselves. 
	
	This function should be called immediately after a successful call to Sgp4PropMse() or Sgp4PropDs50UTC() to retrieve the desired values. 

	It is the caller's responsibility to ensure that the array passed in the destArray parameter is large enough to hold the requested values. The required size can be found by looking at the destArray size column of the table below describing valid index values. 

	The destArray Arrangement column lists the order of the elements in the array. It is not necessarily the subscript of the element in the array since this is language-dependent. For example, in C/C++ the first element in every array is the zero-subscripted element. In other programming languages, the subscript of the first element is 1. 

	Note: This function is not thread safe, please use Sgp4PropAll() instead 

	The table below shows the values for the xf_Sgp4Out parameter:
	index | index Interpretation          | destArray size | destArray Arrangement
	======================================================================
	1     | Revolution number             | 1              | 1. Revolution number (based on the Osculating Keplerian Elements)
	2     | Nodal Apogee Perigee          | 3              | 1. nodal period (minutes)
	      |                               |                | 2. apogee (km)
	      |                               |                | 3. perigee (km)
	3     | Mean Keplerian Elements       | 6              | 1. semi-major axis (km)
	      |                               |                | 2. eccentricity (unitless)
	      |                               |                | 3. inclination (degree)
	      |                               |                | 4. mean anomaly (degree)
	      |                               |                | 5. right ascension of the ascending node (degree)
	      |                               |                | 6. argument of perigee (degree)
	4     | Osculating Keplerian Elements | 6              | Same as Mean Keplerian Elements

	:param settings.stay_int64 satKey: The unique key of the satellite for which to retrieve results.
	:param xf_SgpOut: Specifies which propagator outputs to retrieve. See table above.
	:return int retcode: 0 if the requested information is retrieved successfully, non-0 if there is an error.
	:return list[?] destArr: a list of 1 to 6 elements pulled from the propogator. See table above.
	"""
	
	# test satKey
	if not isinstance(satKey, settings.stay_int64):
		raise TypeError("satKey is type %s, should be type %s" % (type(satKey), settings.stay_int64))
	
	# test xf_Sgp4Out
	if not(xf_Sgp4Out in [1, 2, 3, 4]):
		raise Exception("xf_Sgp4Out is %i, should be 1, 2, 3, or 4. See table in docs." % (xf_Sgp4Out))
	
	# determine length of destArr by means of xf_Sgp4Out and initialize a double array of that length
	xf_Sgp4Out_type_dict = { 1:settings.double1, 2:settings.double3, 3:settings.double6, 4:settings.double6 }
	destArr = xf_Sgp4Out_type_dict[xf_Sgp4Out]()
	
	# set the argtype for Sgp4GetPropOut
	C_SGP4DLL.Sgp4GetPropOut.argtypes = [settings.stay_int64, c.c_int, xf_Sgp4Out_type_dict[xf_Sgp4Out]]
	
	# call Sgp4GetPropOut
	retcode = C_SGP4DLL.Sgp4GetPropOut(satKey, xf_Sgp4Out, destArr)
	
	# convert destArr to a list
	destArr = settings.array_to_list(destArr)
	
	# return values
	return (retcode, destArr)


##Sgp4Init
C_SGP4DLL.Sgp4Init.restype = c.c_int
C_SGP4DLL.Sgp4Init.argtypes = [settings.stay_int64]

def Sgp4Init(apPtr):
	"""
	python:function::Sgp4Init
	Initializes the Sgp4 DLL for use in the program. 
	:param settings.stay_int64 apPtr: The handle that was returned from DllMainInit(). See the documentation for DllMain.dll for details.
	:return int retcode: 0 if Sgp4Prop.dll is initialized successfully, non-0 if there is an error.
	"""
	retcode = C_SGP4DLL.Sgp4Init(apPtr)
	return retcode

##Sgp4InitSat
C_SGP4DLL.Sgp4InitSat.restype = c.c_int
C_SGP4DLL.Sgp4InitSat.argtypes = [settings.stay_int64]

def Sgp4InitSat(satKey):
	"""
	python:function::Sgp4InitSat
	Initializes an SGP4 satellite from an SGP or SGP4 TLE. 
	Internally, when this function is called, Tle.dll's set of TLEs is searched for the provided satKey. If found, the associated TLE data will be used to create an SGP4 satellite which then will be added to Sgp4Prop.dll's set of satellites. Subsequent calls to propagate this satellite will use the data in this set to compute the satellite's new state. 
	This routine should be called once for each satellite you wish to propagate before propagation begins, or any time the associated data that is stored by Tle.dll is changed. 
	The call to this routine needs to be placed before any calls to the SGP4 propagator routines (Sgp4PropMse(), Sgp4PropDs50UTC(), etc.).
	:param settings.stay_int64 satKey: The satellite's unique key. This key will have been returned by one of the routines in Tle.dll.
	:return int retcode: 0 if the satellite is successfully initialized and added to Sgp4Prop.dll's set of satellites, non-0 if there is an error.
	"""
	if not isinstance(satKey, settings.stay_int64):
		raise TypeError("satKey is type %s, should be type %s" % (type(satKey), settings.stay_int64))
	retcode = C_SGP4DLL.Sgp4InitSat(satKey)
	return retcode

##Sgp4PosVelToKep
C_SGP4DLL.Sgp4PosVelToKep.restype = c.c_int
C_SGP4DLL.Sgp4PosVelToKep.argtypes = [c.c_int32,
									  c.c_double,
									  settings.double3,
									  settings.double3,
									  settings.double3,
									  settings.double3,
									  settings.double6]

def Sgp4PosVelToKep(yr, day, pos, vel):
	"""
	python:function::Sgp4PosVelToKep
	Converts osculating position and velocity vectors to a set of mean Keplerian SGP4 elements.
	The new position and velocity vectors are the results of using SGP4 propagator to propagate the computed sgp4MeanKep to the time specified in year and day of epoch time. They should be closely matched with the input osculating position and velocity vectors. 
	The mean Keplerian elements are SGP4's Brouwer mean motion not SGP's Kozai mean motion. 
	:param int yr: 2 or 4 digit year of the epoch time
	:param float day: Day of year of the epoch time.
	:param float[3] pos: Input osculating position vector (km). (double[3])
	:param float[3] vel: Input osculating velocity vector (km/s). (double[3])
	:return int retcode: 0 if the conversion is successful, non-0 if there is an error.
	:return float[3] posNew: Resulting position vector (km) propagated from the sgp4MeanKep. (double[3])
	:return float[3] velNew: Resulting velocity vector (km/s) propagated from the sgp4MeanKep. (double[3])
	:return float[6] sgp4MeanKep: Resulting set of Sgp4 mean Keplerian elements. (double[6])
	"""
	yr = c.c_int32(yr)
	day = c.c_double(day)
	pos = settings.list_to_array(pos)
	vel = settings.list_to_array(vel)
	posNew = settings.double3()
	velNew = settings.double3()
	sgp4MeanKep = settings.double6()
	retcode = C_SGP4DLL.Sgp4PosVelToKep(yr, day, pos, vel, posNew, velNew, sgp4MeanKep)
	posNew = settings.array_to_list(posNew)
	velNew = settings.array_to_list(velNew)
	return (retcode, posNew, velNew, sgp4MeanKep)

##Sgp4PropAll 
##Sgp4PropDs50UTC 
##Sgp4PropDs50UtcLLH 
##Sgp4PropDs50UtcPos 

##Sgp4PropMse 
C_SGP4DLL.Sgp4PropMse.restype = c.c_int
C_SGP4DLL.Sgp4PropMse.argtypes = [settings.stay_int64,
								  c.c_double,
								  c.POINTER(c.c_double),
								  settings.double3,
								  settings.double3,
								  settings.double3]

def Sgp4PropMse(satKey, mse):
	"""
	python:function::Sgp4PropMse
	Propagates a satellite, represented by the satKey, to the time expressed in minutes since the satellite's epoch time. The resulting data about the satellite is placed in the various reference parameters. 
	
	It is the users' responsibility to decide what to do with the returned value. For example, if the users want to check for decay or low altitude, they can put that logic into their own code. 
	This function can be called in random time requests. 
	The following cases will result in an error: 
	1. Semi major axis A <= 0 or A >1.0D6
	2. Eccentricity E >= 1.0 or E < -1.0D-3
	3. Mean anomaly MA>=1.0D10
	4. Hyperbolic orbit E2>= 1.0
	5. satKey doesn't exist in the set of loaded satellites
	6. GEO model not set to WGS-72 and/or FK model not set to FK5
	
	:param settings.stay_int64 satKey: The satellite's unique key.
	:param float mse: The time to propagate to, specified in minutes since the satellite's epoch time.
	:return int retcode: 0 if the propagation is successful, non-0 if there is an error.
	:return float ds50UTC: Resulting time in days since 1950, UTC.
	:return float[3] pos: Resulting ECI position vector (km) in True Equator and Mean Equinox of Epoch. (double[3])
	:return float[3] vel: Resulting ECI velocity vector (km/s) in True Equator and Mean Equinox of Epoch. (double[3])
	:return float[3] llh: Resulting geodetic latitude (deg), longitude(deg), and height (km). (double[3])
	"""
	if not isinstance(satKey, settings.stay_int64):
		raise TypeError("satKey is type %s, should be type %s" % (type(satKey), settings.stay_int64))
	mse = c.c_double(mse)
	ds50UTC = c.c_double(0)
	pos = settings.double3()
	vel = settings.double3()
	llh = settings.double3()
	retcode = C_SGP4DLL.Sgp4PropMse(satKey, mse, c.byref(ds50UTC), pos, vel, llh)
	ds50UTC = ds50UTC.value
	pos = settings.array_to_list(pos)
	vel = settings.array_to_list(vel)
	llh = settings.array_to_list(llh)
	return (retcode, ds50UTC, pos, vel, llh)
	
##Sgp4ReepochTLE 
##Sgp4RemoveAllSats 
##Sgp4RemoveSat 
##Sgp4SetLicFilePath
C_SGP4DLL.Sgp4SetLicFilePath.argtypes = [c.c_char_p]

def Sgp4SetLicFilePath(licFilePath):
	"""
	python:function::Sgp4SetLicFilePath
	Sets path to the Sgp4 Open License file if the license file is not in the current working folder. 
	Note: Remember to call this function even before calling the Sgp4Init. 
	The licFilePath can contain either an absolute or relative path to the 
	folder containing the license file, but it must include a trailing 
	path separator. I.e. "./license/" not "./license" 
	:param str licFilePath: The path to the folder containing the license file, ending in a '/' and not the name of the file itself
	"""
	licFilePath = settings.str_to_c_char_p(licFilePath, fixed_width=None, limit=512, terminator=None)
	C_SGP4DLL.Sgp4SetLicFilePath(licFilePath)
	
