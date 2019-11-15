#! /usr/bin/env python3
from dshsaa.raw import settings, exceptions
import ctypes as c
import pdb

C_TLEDLL = c.CDLL(settings.LIB_TLE_NAME)

##TleAddSatFrArray
C_TLEDLL.TleAddSatFrArray.restype = settings.stay_int64
C_TLEDLL.TleAddSatFrArray.argtypes = [settings.double64, c.c_char_p]
def TleAddSatFrArray(xa_tle, xs_tle):
	"""
	python:function::TleAddSatFrArray
	Adds a TLE (satellite), using its data stored in the input parameters.
	:param float[64] xa_tle: Array containing TLE's numerical fields, see XA_TLE_? for array arrangement (double[64])
	:param str xs_tle: Input string that contains all TLE's text fields, see XS_TLE_? for column arrangement (string[512])
	:return settings.stay_int64 satKey: The satKey of the newly added TLE on success, a negative value on error.
	"""
	xa_tle = settings.list_to_array(xa_tle)
	xs_tle = settings.str_to_c_char_p(xs_tle, fixed_width=512)
	satKey = C_TLEDLL.TleAddSatFrArray(xa_tle, xs_tle)
	return satKey
	
##TleAddSatFrArrayML
C_TLEDLL.TleAddSatFrArrayML.restype = settings.stay_int64
C_TLEDLL.TleAddSatFrArrayML.argtypes = [settings.double64, c.c_char_p]
def TleAddSatFrArrayML(xa_tle, xs_tle):
	"""
	python:function::TleAddSatFrArrayML
	This function is similar to TleAddSatFrArray but designed to be used in Matlab. 
	:param float[64] xa_tle: Array containing TLE's numerical fields, see XA_TLE_? for array arrangement (double[64])
	:param str xs_tle: Input string that contains all TLE's text fields, see XS_TLE_? for column arrangement (string[512])
	:return settings.stay_int64 satKey: The satKey of the newly added TLE on success, a negative value on error.
	"""
	xa_tle = settings.list_to_array(xa_tle)
	xs_tle = settings.str_to_c_char_p(xs_tle, fixed_width=512)
	satKey = C_TLEDLL.TleAddSatFrArrayML(xa_tle, xs_tle)
	return satKey

##TleAddSatFrFieldsGP
C_TLEDLL.TleAddSatFrFieldsGP.restype = settings.stay_int64
C_TLEDLL.TleAddSatFrFieldsGP.argtypes = [c.c_int32, 
										 c.c_char, 
										 c.c_char_p, 
										 c.c_int,
										 c.c_double, 
										 c.c_double, 
										 c.c_int, 
										 c.c_int, 
										 c.c_double, 
										 c.c_double, 
										 c.c_double, 
										 c.c_double, 
										 c.c_double, 
										 c.c_double, 
										 c.c_int]
def TleAddSatFrFieldsGP(satNum, secClass, satName, epochYr, epochDays, bstar, ephType, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum):
	"""
	python:function::TleAddSatFrFieldsGP
	Adds a GP TLE using its individually provided field values.
	:param int satNum: satellite number
	:param str secClass: security classification
	:param str satName: Satellite international designator (string[8])
	:param int epochYr: Element epoch time - year, [YY]YY
	:param float epochDays: Element epoch time - day of year, DDD.DDDDDDDD
	:param float bstar: B* drag term (1/er)
	:param int ephType: Satellite ephemeris type (0: SGP, 2: SGP4)
	:param int elsetNum: element set number
	:param float incli: orbit inclination (degrees)
	:param float node: right ascension of ascending node (degrees)
	:param float eccen: eccentricity
	:param float omega: argument of perigee (degrees)
	:param float mnAnomaly: mean anomaly (degrees)
	:param float mnMotion: mean motion (rev/day) (ephType = 0: Kozai mean motion, ephType = 2: Brouwer mean motion)
	:param int revNum: revolution number at epoch
	:return satKey: The satKey of the newly added TLE on success, a negative value on error.
	"""
	satNum = c.c_int(satNum)
	secClass = c.c_char(secClass.encode('ascii', 'strict'))
	satName = settings.str_to_c_char_p(satName, fixed_width=8)
	epochYr = c.c_int(epochYr)
	epochDays = c.c_double(epochDays)
	bstar = c.c_double(bstar)
	ephType = c.c_int32(ephType)
	elsetNum = c.c_int32(elsetNum)
	incli = c.c_double(incli)
	node = c.c_double(node)
	eccen = c.c_double(eccen)
	omega = c.c_double(omega)
	mnAnomaly = c.c_double(mnAnomaly)
	mnMotion = c.c_double(mnMotion)
	revNum = c.c_int32(revNum)
	satKey = C_TLEDLL.TleAddSatFrFieldsGP(satNum, secClass, satName, epochYr, epochDays, bstar, ephType, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum)
	return satKey

##TleAddSatFrFieldsGP2
C_TLEDLL.TleAddSatFrFieldsGP2.restype = settings.stay_int64
C_TLEDLL.TleAddSatFrFieldsGP2.argtypes = [c.c_int32, 
										 c.c_char, 
										 c.c_char_p, 
										 c.c_int,
										 c.c_double, 
										 c.c_double, 
										 c.c_int, 
										 c.c_int, 
										 c.c_double, 
										 c.c_double, 
										 c.c_double, 
										 c.c_double, 
										 c.c_double, 
										 c.c_double, 
										 c.c_int,
										 c.c_double,
										 c.c_double]
def TleAddSatFrFieldsGP2(satNum, secClass, satName, epochYr, epochDays, bstar, ephType, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum, nDotO2, n2DotO6):
	"""
	python:function::TleAddSatFrFieldsGP2
	This function is similar to TleAddSatFrFieldsGP but includes nDotO2 and n2DotO6. nDotO2 and n2DotO6 values are not used in the SGP4 propagator. However, some users still want to preserve the integrity of all input data. 
	:param int satNum: satellite number
	:param str secClass: security classification
	:param str satName: Satellite international designator (string[8])
	:param int epochYr: Element epoch time - year, [YY]YY
	:param float epochDays: Element epoch time - day of year, DDD.DDDDDDDD
	:param float bstar: B* drag term (1/er)
	:param int ephType: Satellite ephemeris type (0: SGP, 2: SGP4)
	:param int elsetNum: element set number
	:param float incli: orbit inclination (degrees)
	:param float node: right ascension of ascending node (degrees)
	:param float eccen: eccentricity
	:param float omega: argument of perigee (degrees)
	:param float mnAnomaly: mean anomaly (degrees)
	:param float mnMotion: mean motion (rev/day) (ephType = 0: Kozai mean motion, ephType = 2: Brouwer mean motion)
	:param int revNum: revolution number at epoch
	:param float nDotO2: Mean motion derivative (rev/day /2)
	:param float n2DotO6: Mean motion second derivative (rev/day**2 /6)
	:return satKey: 
	"""
	satNum = c.c_int(satNum)
	secClass = c.c_char(secClass.encode('ascii', 'strict'))
	satName = settings.str_to_c_char_p(satName, fixed_width=8)
	epochYr = c.c_int(epochYr)
	epochDays = c.c_double(epochDays)
	bstar = c.c_double(bstar)
	ephType = c.c_int32(ephType)
	elsetNum = c.c_int32(elsetNum)
	incli = c.c_double(incli)
	node = c.c_double(node)
	eccen = c.c_double(eccen)
	omega = c.c_double(omega)
	mnAnomaly = c.c_double(mnAnomaly)
	mnMotion = c.c_double(mnMotion)
	revNum = c.c_int32(revNum)
	nDotO2 = c.c_double(nDotO2)
	n2DotO6 = c.c_double(n2DotO6)
	satKey = C_TLEDLL.TleAddSatFrFieldsGP2(satNum, secClass, satName, epochYr, epochDays, bstar, ephType, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum, nDotO2, n2DotO6)
	return satKey
	
	
##TleAddSatFrFieldsGP2ML
C_TLEDLL.TleAddSatFrFieldsGP2ML.restype = settings.stay_int64
C_TLEDLL.TleAddSatFrFieldsGP2ML.argtypes = [c.c_int32, 
										 c.c_char, 
										 c.c_char_p, 
										 c.c_int,
										 c.c_double, 
										 c.c_double, 
										 c.c_int, 
										 c.c_int, 
										 c.c_double, 
										 c.c_double, 
										 c.c_double, 
										 c.c_double, 
										 c.c_double, 
										 c.c_double, 
										 c.c_int,
										 c.c_double,
										 c.c_double]
def TleAddSatFrFieldsGP2ML(satNum, secClass, satName, epochYr, epochDays, bstar, ephType, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum, nDotO2, n2DotO6):
	"""
	python:function::TleAddSatFrFieldsGP2ML
	This function is similar to TleAddSatFrFieldsGP2 but designed to be used in Matlab. Matlab doesn't seem to correctly return the 19-digit satellite key using TleAddSatFrFieldsGP2. This method is an alternative way to return the satKey output. This function is similar to TleAddSatFrFieldsGP but includes nDotO2 and n2DotO6. nDotO2 and n2DotO6 values are not used in the SGP4 propagator. However, some users still want to preserve the integrity of all input data. 
	:param int satNum: satellite number
	:param str secClass: security classification
	:param str satName: Satellite international designator (string[8])
	:param int epochYr: Element epoch time - year, [YY]YY
	:param float epochDays: Element epoch time - day of year, DDD.DDDDDDDD
	:param float bstar: B* drag term (1/er)
	:param int ephType: Satellite ephemeris type (0: SGP, 2: SGP4)
	:param int elsetNum: element set number
	:param float incli: orbit inclination (degrees)
	:param float node: right ascension of ascending node (degrees)
	:param float eccen: eccentricity
	:param float omega: argument of perigee (degrees)
	:param float mnAnomaly: mean anomaly (degrees)
	:param float mnMotion: mean motion (rev/day) (ephType = 0: Kozai mean motion, ephType = 2: Brouwer mean motion)
	:param int revNum: revolution number at epoch
	:param float nDotO2: Mean motion derivative (rev/day /2)
	:param float n2DotO6: Mean motion second derivative (rev/day**2 /6)
	:return satKey: 
	"""
	satNum = c.c_int(satNum)
	secClass = c.c_char(secClass.encode('ascii', 'strict'))
	satName = settings.str_to_c_char_p(satName, fixed_width=8)
	epochYr = c.c_int(epochYr)
	epochDays = c.c_double(epochDays)
	bstar = c.c_double(bstar)
	ephType = c.c_int32(ephType)
	elsetNum = c.c_int32(elsetNum)
	incli = c.c_double(incli)
	node = c.c_double(node)
	eccen = c.c_double(eccen)
	omega = c.c_double(omega)
	mnAnomaly = c.c_double(mnAnomaly)
	mnMotion = c.c_double(mnMotion)
	revNum = c.c_int32(revNum)
	nDotO2 = c.c_double(nDotO2)
	n2DotO6 = c.c_double(n2DotO6)
	satKey = C_TLEDLL.TleAddSatFrFieldsGP2ML(satNum, secClass, satName, epochYr, epochDays, bstar, ephType, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum, nDotO2, n2DotO6)
	return satKey


##TleAddSatFrFieldsSP
C_TLEDLL.TleAddSatFrFieldsSP.restype = settings.stay_int64
C_TLEDLL.TleAddSatFrFieldsSP.argtypes = [c.c_int32,
										 c.c_char,
										 c.c_char_p,
										 c.c_int32,
										 c.c_double,
										 c.c_double,
										 c.c_double,
										 c.c_double,
										 c.c_int32,
										 c.c_double,
										 c.c_double,
										 c.c_double,
										 c.c_double,
										 c.c_double,
										 c.c_double,
										 c.c_int32]
def TleAddSatFrFieldsSP(satNum, secClass, satName, epochYr, epochDays, bTerm, ogParm, agom, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum):
	"""
	python:function::TleAddSatFrFieldsSP
	Adds an SP satellite using the individually provided field values. Only applies to SP propagator.
	Review https://www.sat.dundee.ac.uk/fle.html for more information on SP 4 line element sets.
	:param int satNum: Satellite number
	:param str secClass: Security classification
	:param str satName: Satellite international designator (string[8])
	:param int epochYr: Element epoch time - year, [YY]YY
	:param float epochDays: Element epoch time - day of year, DDD.DDDDDDDD
	:param float bTerm: Ballistic coefficient (m^2/kg)
	:param float ogParm: Outgassing parameter/Thrust Acceleration (km/s^2)
	:param float agom: Agom (radiation pressure coefficient) (m^2/kg)
	:param int elsetNum: Element set number
	:param float incli: Orbit inclination (degrees)
	:param float node: Right ascension of ascending node (degrees)
	:param float eccen: Eccentricity
	:param float omega: Argument of perigee (degrees)
	:param float mnAnomaly: Mean anomaly (degrees)
	:param float mnMotion: Mean motion (rev/day)
	:param int revNum: Revolution number at epoch
	:return settings.stay_int64 satKey: The satKey of the newly added TLE on success, a negative value on error.
	"""
	satNum = c.c_int32(satNum)
	secClass = c.c_char(secClass.encode('ascii', 'strict'))
	satName = settings.str_to_c_char_p(satName, fixed_width=8)
	epochYr = c.c_int(epochYr)
	epochDays = c.c_double(epochDays)
	bTerm = c.c_double(bTerm)
	ogParm = c.c_double(ogParm)
	agom = c.c_double(agom)
	elsetNum = c.c_int32(elsetNum)
	incli = c.c_double(incli)
	node = c.c_double(node)
	eccen = c.c_double(eccen)
	omega = c.c_double(omega)
	mnAnomaly = c.c_double(mnAnomaly)
	mnMotion = c.c_double(mnMotion)
	revNum = c.c_int32(revNum)
	satKey = C_TLEDLL.TleAddSatFrFieldsSP(satNum, secClass, satName, epochYr, epochDays, bTerm, ogParm, agom, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum)
	return satKey
	
##TleAddSatFrFieldsSPML
C_TLEDLL.TleAddSatFrFieldsSPML.restype = settings.stay_int64
C_TLEDLL.TleAddSatFrFieldsSPML.argtypes = [c.c_int32,
										 c.c_char,
										 c.c_char_p,
										 c.c_int32,
										 c.c_double,
										 c.c_double,
										 c.c_double,
										 c.c_double,
										 c.c_int32,
										 c.c_double,
										 c.c_double,
										 c.c_double,
										 c.c_double,
										 c.c_double,
										 c.c_double,
										 c.c_int32]
def TleAddSatFrFieldsSPML(satNum, secClass, satName, epochYr, epochDays, bTerm, ogParm, agom, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum):
	"""
	python:function::TleAddSatFrFieldsSPML
	Adds an SP satellite using the individually provided field values. This function is similar to TleAddSatFrFieldsSP but designed to be used in Matlab. Matlab doesn't correctly return the 19-digit satellite key using TleAddSatFrFieldsSP. This method is an alternative way to return the satKey output. Only applies to SP propagator.
	Review https://www.sat.dundee.ac.uk/fle.html for more information on SP 4 line element sets.
	:param int satNum: Satellite number
	:param str secClass: Security classification
	:param str satName: Satellite international designator (string[8])
	:param int epochYr: Element epoch time - year, [YY]YY
	:param float epochDays: Element epoch time - day of year, DDD.DDDDDDDD
	:param float bTerm: Ballistic coefficient (m^2/kg)
	:param float ogParm: Outgassing parameter/Thrust Acceleration (km/s^2)
	:param float agom: Agom (radiation pressure coefficient) (m^2/kg)
	:param int elsetNum: Element set number
	:param float incli: Orbit inclination (degrees)
	:param float node: Right ascension of ascending node (degrees)
	:param float eccen: Eccentricity
	:param float omega: Argument of perigee (degrees)
	:param float mnAnomaly: Mean anomaly (degrees)
	:param float mnMotion: Mean motion (rev/day)
	:param int revNum: Revolution number at epoch
	:return settings.stay_int64 satKey: The satKey of the newly added TLE on success, a negative value on error.
	"""
	satNum = c.c_int32(satNum)
	secClass = c.c_char(secClass.encode('ascii', 'strict'))
	satName = settings.str_to_c_char_p(satName, fixed_width=8)
	epochYr = c.c_int(epochYr)
	epochDays = c.c_double(epochDays)
	bTerm = c.c_double(bTerm)
	ogParm = c.c_double(ogParm)
	agom = c.c_double(agom)
	elsetNum = c.c_int32(elsetNum)
	incli = c.c_double(incli)
	node = c.c_double(node)
	eccen = c.c_double(eccen)
	omega = c.c_double(omega)
	mnAnomaly = c.c_double(mnAnomaly)
	mnMotion = c.c_double(mnMotion)
	revNum = c.c_int32(revNum)
	satKey = C_TLEDLL.TleAddSatFrFieldsSPML(satNum, secClass, satName, epochYr, epochDays, bTerm, ogParm, agom, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum)
	return satKey

##TleAddSatFrLines
C_TLEDLL.TleAddSatFrLines.restype = settings.stay_int64
C_TLEDLL.TleAddSatFrLines.argtypes = [c.c_char_p, c.c_char_p]
def TleAddSatFrLines(line1, line2):
	"""
	python:function::TleAddSatFrArray
	Adds a TLE (satellite), using its directly specified first and second lines.
	Note: Adding two sets of TLEs which are exactly the same will cause the second initialization to fail. Make them distinct by modifying the satellite ID.
	:param str line1: The first line of a two line element set. (string[512])
	:param str line2: The second line of a two line element set (string[512])
	:param settings.stay_int64 satKey: The satKey of the newly added TLE on success, a negative value on error.
	"""
	line1 = settings.str_to_c_char_p(line1, fixed_width=None, limit=None, terminator=None)
	line2 = settings.str_to_c_char_p(line2, fixed_width=None, limit=None, terminator=None)
	satKey = C_TLEDLL.TleAddSatFrLines(line1, line2)
	return satKey

##TleAddSatFrLinesML
C_TLEDLL.TleAddSatFrLinesML.restype = settings.stay_int64
C_TLEDLL.TleAddSatFrLinesML.argtypes = [c.c_char_p, c.c_char_p]
def TleAddSatFrLinesML(line1, line2):
	"""
	python:function::TleAddSatFrArray
	Adds a TLE (satellite), using its directly specified first and second lines.This function is similar to TleAddSatFrLines but designed to be used in Matlab. Matlab doesn't correctly return the 19-digit satellite key using TleAddSatFrLines. This method is an alternative way to return the satKey output. 
	Note: Adding two sets of TLEs which are exactly the same will cause the second initialization to fail. Make them distinct by modifying the satellite ID.
	:param str line1: The first line of a two line element set. (string[512])
	:param str line2: The second line of a two line element set (string[512])
	:param settings.stay_int64 satKey: The satKey of the newly added TLE on success, a negative value on error.
	"""
	line1 = settings.str_to_c_char_p(line1, fixed_width=None, limit=None, terminator=None)
	line2 = settings.str_to_c_char_p(line2, fixed_width=None, limit=None, terminator=None)
	satKey = C_TLEDLL.TleAddSatFrLinesML(line1, line2)
	return satKey

##TleDataToArray
C_TLEDLL.TleDataToArray.restype = c.c_int
C_TLEDLL.TleDataToArray.argtypes = [settings.stay_int64, settings.double64, c.c_char_p]
def TleDataToArray(satKey):
	"""
	python:function::TleDataToArray
	Retrieves TLE data and stored it in the passing parameters 
	:param settings.stay_int64 satKey: The satellite's unique key
	:return int retcode: 0 if all values are retrieved successfully, non-0 if there is an error
	:return float[64] xa_tle: Array containing TLE's numerical fields, see XA_TLE_? for array arrangement (double[64])
	:return str xs_tle: Output string that contains all TLE's text fields, see XS_TLE_? for column arrangement (byte[512])
	"""
	if not isinstance(satKey, settings.stay_int64):
		raise TypeError("satKey is type %s, should be type %s" % (type(satKey), settings.stay_int64))
	xa_tle = settings.double64()
	xs_tle = c.c_char_p(bytes(512))
	retcode = C_TLEDLL.TleDataToArray(satKey, xa_tle, xs_tle)
	xa_tle = settings.array_to_list(xa_tle)
	xs_tle = settings.byte_to_str(xs_tle)
	return (retcode	, xa_tle, xs_tle)
	
##TleFieldsToSatKey
C_TLEDLL.TleFieldsToSatKey.restype = settings.stay_int64
C_TLEDLL.TleFieldsToSatKey.argtypes = [c.c_int32, c.c_int32, c.c_double, c.c_int32]
def TleFieldsToSatKey(satNum, epochYr, epochDays, ephType):
	"""
	python:function::TleFieldsToSatKey
	Computes a satKey from the input data.
	There is no need for a matching satellite to be loaded prior to using this function. The function simply computes the satKey from the provided fields. 
	This is the proper way to reconstruct a satKey from its fields. If you use your own routine to do this, the computed satKey might be different. 
	A negative value will be returned if there is an error. 
	:param int satNum: Satellite number
	:param int epochYr: Element epoch time - year, [YY]YY
	:param float epochDays: Element epoch time - day of year, DDD.DDDDDDDD
	:param int ephType: Ephemeris type
	:return settings.stay_int64 satKey: The resulting satellite key if the computation is successful; a negative value if there is an error.
	"""
	satNum = c.c_int32(satNum)
	epochYr = c.c_int32(epochYr)
	epochDays = c.c_double(epochDays)
	ephType = c.c_int32(ephType)
	satKey = C_TLEDLL.TleFieldsToSatKey(satNum, epochYr, epochDays, ephType)
	return satKey

##TleFieldsToSatKeyML
C_TLEDLL.TleFieldsToSatKeyML.restype = settings.stay_int64
C_TLEDLL.TleFieldsToSatKeyML.argtypes = [c.c_int32, c.c_int32, c.c_double, c.c_int32]
def TleFieldsToSatKeyML(satNum, epochYr, epochDays, ephType):
	"""
	python:function::TleFieldsToSatKeyML
	This function is similar to TleFieldsToSatKey but designed to be used in Matlab. Computes a satKey from the input data.
	There is no need for a matching satellite to be loaded prior to using this function. The function simply computes the satKey from the provided fields. 
	This is the proper way to reconstruct a satKey from its fields. If you use your own routine to do this, the computed satKey might be different. 
	A negative value will be returned if there is an error. 
	:param int satNum: Satellite number
	:param int epochYr: Element epoch time - year, [YY]YY
	:param float epochDays: Element epoch time - day of year, DDD.DDDDDDDD
	:param int ephType: Ephemeris type
	:return settings.stay_int64 satKey: The resulting satellite key if the computation is successful; a negative value if there is an error.
	"""
	satNum = c.c_int32(satNum)
	epochYr = c.c_int32(epochYr)
	epochDays = c.c_double(epochDays)
	ephType = c.c_int32(ephType)
	satKey = C_TLEDLL.TleFieldsToSatKeyML(satNum, epochYr, epochDays, ephType)
	return satKey

##TleGetAllFieldsGP
C_TLEDLL.TleGetAllFieldsGP.restype = c.c_int
C_TLEDLL.TleGetAllFieldsGP.argtypes = [settings.stay_int64,
									   c.POINTER(c.c_int32),
									   c.POINTER(c.c_char),
									   c.c_char_p,
									   c.POINTER(c.c_int32),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_int32),
									   c.POINTER(c.c_int32),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double), 
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_int32)]
def TleGetAllFieldsGP(satKey):
	"""
	python:function::TleGetAllFieldsGP
	Retrieves all of the data for a GP satellite in a single function call.
	This function only works for GP satellites. The field values are placed in the corresponding parameters of the function. 
	:param settings.stay_int64 satKey: The satellite's unique key
	:return int retcode: 0 if all values are retrieved successfully, non-0 if there is an error.
	:return int satNum: Satellite number
	:return str secClass: Security classification
	:return str satName: Satellite international designator (byte[8])
	:return int epochYr: Element epoch time - year, [YY]YY
	:return float epochDays: Element epoch time - day of year, DDD.DDDDDDDD
	:return float bstar: B* drag term (1/er)
	:return int ephType: Satellite ephemeris type (0: SGP, 2: SGP4, 6: SP)
	:return int elsetNum: Element set number
	:return float incli: Orbit inclination (degrees)
	:return float node: Right ascension of ascending node (degrees)
	:return float eccen: Eccentricity
	:return float omega: Argument of perigee (degrees)
	:return float mnAnomaly: Mean anomaly (deg)
	:return float mnMotion: Mean motion (rev/day) (ephType = 0: Kozai mean motion, ephType = 2: Brouwer mean motion)
	:return int revNum: Revolution number at epoch
	"""
	if not isinstance(satKey, settings.stay_int64):
		raise TypeError("satKey is type %s, should be type %s" % (type(satKey), settings.stay_int64))
	satNum    = c.c_int32()
	secClass  = c.c_char(b' ')
	satName   = settings.str_to_c_char_p('        ', fixed_width=8)
	epochYr   = c.c_int32()
	epochDays = c.c_double()
	bstar     = c.c_double()
	ephType   = c.c_int32()
	elsetNum  = c.c_int32()
	incli     = c.c_double()
	node      = c.c_double()
	eccen     = c.c_double()
	omega     = c.c_double()
	mnAnomaly = c.c_double()
	mnMotion  = c.c_double()
	revNum    = c.c_int32()
	retcode   = C_TLEDLL.TleGetAllFieldsGP(
		satKey.value,
		c.byref(satNum),
		c.byref(secClass),
		satName,
		c.byref(epochYr),
		c.byref(epochDays),
		c.byref(bstar),
		c.byref(ephType),
		c.byref(elsetNum),
		c.byref(incli),
		c.byref(node),
		c.byref(eccen),
		c.byref(omega),
		c.byref(mnAnomaly),
		c.byref(mnMotion),
		c.byref(revNum))
	satNum    = satNum.value
	secClass  = secClass.value
	secClass  = secClass.decode('ascii')
	satName   = settings.byte_to_str(satName)
	epochYr   = epochYr.value
	epochDays = epochDays.value
	bstar     = bstar.value
	ephType   = ephType.value
	elsetNum  = elsetNum.value
	incli     = incli.value
	node      = node.value
	eccen     = eccen.value
	omega     = omega.value
	mnAnomaly = mnAnomaly.value
	mnMotion  = mnMotion.value
	revNum    = revNum.value
	return (retcode, satNum, secClass, satName, epochYr, epochDays, bstar, ephType, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum)
	
##TleGetAllFieldsGP2
C_TLEDLL.TleGetAllFieldsGP2.restype = c.c_int
C_TLEDLL.TleGetAllFieldsGP2.argtypes = [settings.stay_int64,
									   c.POINTER(c.c_int32),
									   c.POINTER(c.c_char),
									   c.c_char_p,
									   c.POINTER(c.c_int32),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_int32),
									   c.POINTER(c.c_int32),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double), 
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_int32), 
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double)]
def TleGetAllFieldsGP2(satKey):
	"""
	python:function::TleGetAllFieldsGP2
	Retrieves all of the data (including nDotO2 and n2DotO6) for a GP satellite in a single function call. 
	This function only works for GP satellites. The field values are placed in the corresponding parameters of the function. 
	This function is similar to TleGetAllFieldsGP but also includes nDotO2 and n2DotO6. 
	:param settings.stay_int64 satKey: The satellite's unique key
	:return int retcode: 0 if all values are retrieved successfully, non-0 if there is an error.
	:return int satNum: Satellite number
	:return str secClass: Security classification
	:return str satName: Satellite international designator (byte[8])
	:return int epochYr: Element epoch time - year, [YY]YY
	:return float epochDays: Element epoch time - day of year, DDD.DDDDDDDD
	:return float bstar: B* drag term (1/er)
	:return int ephType: Satellite ephemeris type (0: SGP, 2: SGP4, 6: SP)
	:return int elsetNum: Element set number
	:return float incli: Orbit inclination (degrees)
	:return float node: Right ascension of ascending node (degrees)
	:return float eccen: Eccentricity
	:return float omega: Argument of perigee (degrees)
	:return float mnAnomaly: Mean anomaly (deg)
	:return float mnMotion: Mean motion (rev/day) (ephType = 0: Kozai mean motion, ephType = 2: Brouwer mean motion)
	:return int revNum: Revolution number at epoch
	:return float nDotO2: Mean motion derivative (rev/day /2)
	:return float n2DotO6: Mean motion second derivative (rev/day**2 /6)
	"""
	if not isinstance(satKey, settings.stay_int64):
		raise TypeError("satKey is type %s, should be type %s" % (type(satKey), settings.stay_int64))
	satNum    = c.c_int32()
	secClass  = c.c_char()
	satName   = c.c_char_p(bytes(8))
	epochYr   = c.c_int32()
	epochDays = c.c_double()
	bstar     = c.c_double()
	ephType   = c.c_int32()
	elsetNum  = c.c_int32()
	incli     = c.c_double()
	node      = c.c_double()
	eccen     = c.c_double()
	omega     = c.c_double()
	mnAnomaly = c.c_double()
	mnMotion  = c.c_double()
	revNum    = c.c_int32()
	nDotO2    = c.c_double()
	n2DotO6   = c.c_double()
	retcode   = C_TLEDLL.TleGetAllFieldsGP2(
		satKey.value,
		c.byref(satNum),
		c.byref(secClass),
		satName,
		c.byref(epochYr),
		c.byref(epochDays),
		c.byref(bstar),
		c.byref(ephType),
		c.byref(elsetNum),
		c.byref(incli),
		c.byref(node),
		c.byref(eccen),
		c.byref(omega),
		c.byref(mnAnomaly),
		c.byref(mnMotion),
		c.byref(revNum),
		c.byref(nDotO2),
		c.byref(n2DotO6))
	satNum    = satNum.value
	secClass  = secClass.value
	secClass  = secClass.decode('ascii')
	satName   = settings.byte_to_str(satName)
	epochYr   = epochYr.value
	epochDays = epochDays.value
	bstar     = bstar.value
	ephType   = ephType.value
	elsetNum  = elsetNum.value
	incli     = incli.value
	node      = node.value
	eccen     = eccen.value
	omega     = omega.value
	mnAnomaly = mnAnomaly.value
	mnMotion  = mnMotion.value
	revNum    = revNum.value
	nDotO2    = nDotO2.value
	n2DotO6   = n2DotO6.value
	return (retcode, satNum, secClass, satName, epochYr, epochDays, bstar, ephType, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum, nDotO2, n2DotO6)

##TleGetAllFieldsSP
C_TLEDLL.TleGetAllFieldsSP.restype = c.c_int
C_TLEDLL.TleGetAllFieldsSP.argtypes = [settings.stay_int64,
									   c.POINTER(c.c_int32),
									   c.POINTER(c.c_char),
									   c.c_char_p,
									   c.POINTER(c.c_int32),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_int32),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_double),
									   c.POINTER(c.c_int32)]
def TleGetAllFieldsSP(satKey):
	"""
	python:function::TleGetAllFieldsSP
	Retrieves all of the data for an SP satellite in a single function call. Only applies to SP propagator. 
	This function only works for SP satellites. The field values are placed in the corresponding parameters of the function. 
	:param settings.stay_int64 satKey: The satellite's unique key
	:return int retcode: 0 if all values are retrieved successfully, non-0 if there is an error.
	:return int satNum: Satellite number
	:return str secClass: Security classification
	:return str satname: Satellite international designator (byte[8])
	:return int epochYr: Element epoch time - year, [YY]YY
	:return float epochDays: Element epoch time - day of year, DDD.DDDDDDDD
	:return float bTerm: Ballistic coefficient (m^2/kg)
	:return float ogParm: Outgassing parameter/Thrust Acceleration (km/s^2)
	:return float agom: Agom (m^2/kg)
	:return int elsetNum: Element set number
	:return float incli: Orbit inclination (degrees)
	:return float node: Right ascension of ascending node (degrees)
	:return float eccen: Eccentricity
	:return float omega: Argument of perigee (degrees)
	:return float mnAnomaly: Mean anomaly (degrees)
	:return float mnMotion: Mean motion (rev/day)
	:return int revNum: Revolution number at epoch
	"""
	if not isinstance(satKey, settings.stay_int64):
		raise TypeError("satKey is type %s, should be type %s" % (type(satKey), settings.stay_int64))
	satNum    = c.c_int32()
	secClass  = c.c_char()
	satName   = c.c_char_p(bytes(8))
	epochYr   = c.c_int32()
	epochDays = c.c_double()
	bTerm     = c.c_double()
	ogParm    = c.c_double()
	agom     = c.c_double()
	elsetNum  = c.c_int32()
	incli     = c.c_double()
	node      = c.c_double()
	eccen     = c.c_double()
	omega     = c.c_double()
	mnAnomaly = c.c_double()
	mnMotion  = c.c_double()
	revNum    = c.c_int32()
	retcode   = C_TLEDLL.TleGetAllFieldsSP(
		satKey,
		c.byref(satNum),
		c.byref(secClass),
		satName,
		c.byref(epochYr),
		c.byref(epochDays),
		c.byref(bTerm),
		c.byref(ogParm),
		c.byref(agom),
		c.byref(elsetNum),
		c.byref(incli),
		c.byref(node),
		c.byref(eccen),
		c.byref(omega),
		c.byref(mnAnomaly),
		c.byref(mnMotion),
		c.byref(revNum))
	satNum    = satNum.value
	secClass  = secClass.value
	secClass  = secClass.decode('ascii')
	satName   = settings.byte_to_str(satName)
	epochYr   = epochYr.value
	epochDays = epochDays.value
	bTerm     = bTerm.value
	ogParm    = ogParm.value
	agom      = agom.value
	elsetNum  = elsetNum.value
	incli     = incli.value
	node      = node.value
	eccen     = eccen.value
	omega     = omega.value
	mnAnomaly = mnAnomaly.value
	mnMotion  = mnMotion.value
	revNum    = revNum.value
	return (retcode, satNum, secClass, satName, epochYr, epochDays, bTerm, ogParm, agom, elsetNum, incli, node, eccen, omega, mnAnomaly, mnMotion, revNum)
	
##TleGetCount
C_TLEDLL.TleGetCount.restype = c.c_int
def TleGetCount():
	"""
	python:function::TleGetCount
	Returns the number of TLEs currently loaded. 
	See TleGetLoaded for an example. 
	This function is useful for dynamically allocating memory for the array that is passed to the function TleGetLoaded(). 
	:return int tle_count: The number of TLEs currently loaded.
	"""
	tle_count = C_TLEDLL.TleGetCount()
	return tle_count

##TleGetField
C_TLEDLL.TleGetField.restype = c.c_int
C_TLEDLL.TleGetField.argtypes = [settings.stay_int64, c.c_int32, c.c_char_p]
def TleGetField(satKey, xf_Tle):
	"""
	python:function::TleGetField
	Retrieves the value of a specific field of a TLE. 
	The table below indicates which index values correspond to which fields. Make sure to use the appropriate field index for GP TLEs and SP TLEs. For indexes 5, 15 and 16, the interpretation depends on the ephemeris type of the TLE. 
	index | index Interpretation
	============================
	1 | Satellite number
	2 | Security classification
	3 | Satellite international designator
	4 | Epoch
	5 | Ephemeris type = 0,2: B* drag term (1/er), Ephemeris type = 6 : SP radiation pressure coefficient Agom (m2/kg)
	6 | Ephemeris type
	7 | Element set number
	8 | Orbit inclination (degrees)
	9 | Right ascension of ascending node (degrees)
	10 | Eccentricity
	11 | Argument of perigee (degrees)
	12 | Mean anomaly (degrees)
	13 | Mean motion (rev/day)
	14 | Revolution number at epoch
	15 | Ephemeris type = 0: SGP mean motion derivative (rev/day /2) or Ephemeris type = 6: SP ballistic coefficient (m2/kg)
	16 | Ephemeris type = 0: SGP mean motion second derivative (rev/day**2 /6) or Ephemeris type = 6: SP Outgassing parameter/Thrust Acceleration (km/s2)
	:param settings.stay_int64 satKey: The satellite's unique key.
	:param int xf_Tle: Predefined number specifying which field to retrieve. See remarks.
	:return int retcode: 0 if the TLE data is successfully retrieved, non-0 if there is an error.
	:return str valueStr: A string to contain the value of the requested field. (byte[512])
	"""
	if not isinstance(satKey, settings.stay_int64):
		raise TypeError("satKey is type %s, should be type %s" % (type(satKey), settings.stay_int64))
	xf_Tle = c.c_int32(xf_Tle)
	valueStr = c.c_char_p(bytes(512))
	retcode = C_TLEDLL.TleGetField(satKey, xf_Tle, valueStr)
	valueStr = settings.byte_to_str(valueStr)
	return (retcode, valueStr)







##TleGetInfo
##TleGetLines
##TleGetLoaded
##TleGetSatKey
##TleGetSatKeyML
##TleGPArrayToLines
##TleGPFieldsToLines

##TleInit
C_TLEDLL.TleInit.restype = c.c_int64
C_TLEDLL.TleInit.argtypes = [settings.stay_int64]
def TleInit(apPtr):
	"""
	python:function::TleInit
	Initializes Tle DLL for use in the program.
	:param settings.stay_int64 apPtr: The handle that was returned from DllMainInit. See the documentation for DllMain.dll for details.
	:return int retcode: 0 if Tle.dll is initialized successfully, non-0 if there is an error.
	"""
	retcode = C_TLEDLL.TleInit(apPtr)
	return retcode

##TleLinesToArray
C_TLEDLL.TleLinesToArray.restype = c.c_int64
C_TLEDLL.TleLinesToArray.argtypes = [c.c_char_p] * 2 + [settings.double64] + [c.c_char_p]
def TleLinesToArray(line1, line2):
	"""
	python:function::TleLinesToArray
	Parses GP data from the input first and second lines of a two line element set and store that data back into the output parameters. 
	This function only parses data from the input TLE but DOES NOT load/add the input TLE to memory. 
	:param str line1: The first line of the two line element set. (string[512])
	:param str line2: The second line of the two line element set (if needed, line3 can be inserted into line2's 101-180th column). (string[512])
	:return float[64] xa_tle: Array containing TLE's numerical fields, see XA_TLE_? for array arrangement (double[64])
	:return str xs_tle: Output string that contains all TLE's text fields, see XS_TLE_? for column arrangement (byte[512])
	:return int retcode: 0 if the TLE is parsed successfully, non-0 if there is an error.
	"""
	line1 = settings.str_to_c_char_p(line1, fixed_width=None, limit=None, terminator=None)
	line2 = settings.str_to_c_char_p(line2, fixed_width=None, limit=None, terminator=None)
	xa_tle = settings.double64()
	xs_tle = c.c_char_p(bytes(512))
	retcode = C_TLEDLL.TleLinesToArray(line1, line2, xa_tle, xs_tle)
	xa_tle = settings.array_to_list(xa_tle)
	xs_tle = settings.byte_to_str(xs_tle)
	return (retcode, xa_tle, xs_tle)



##TleLoadFile
##TleParseGP
##TleParseSP
##TleRemoveAllSats
C_TLEDLL.TleRemoveAllSats.restype = c.c_int
def TleRemoveAllSats():
	"""
	python:function::TleRemoveAllSats
	Removes all the TLEs from memory.
	:return int retcode: 0 if all TLE's are removed successfully from memory, non-0 if there is an error.
	"""
	retcode = C_TLEDLL.TleRemoveAllSats()
	return retcode

##TleRemoveSat
##TleSaveFile
##TleSetField
##TleSPFieldsToLines
##TleUpdateSatFrArray
##TleUpdateSatFrFieldsGP
##TleUpdateSatFrFieldsGP2
##TleUpdateSatFrFieldsSP
