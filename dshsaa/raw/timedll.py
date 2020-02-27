#! /usr/bin/env python3

import dshsaa.raw.settings as settings
import ctypes as c
import pdb

C_TIMEDLL = c.CDLL(settings.LIB_TIME_NAME)

# The pattern for the rest of this file will be:
# 1. Set parameter types
# 2. Set return types
# 3. Define a python-friendly function

## DTGToUTC
C_TIMEDLL.DTGToUTC.restype = c.c_double
C_TIMEDLL.DTGToUTC.argtypes = [c.c_char_p]
def DTGToUTC(dtg):
	"""
	Converts a time in one of the DTG formats to a time in ds50UTC. DTG15, DTG17, DTG19, and DTG20 formats are accepted. 

	..Note:: See "UTCToDTG20" for an example. 

	During the conversion, this function processes only numbers and the '.' character. This means that you can format dtgStr in a format that makes sense. You can use spaces and the '/' character for example if you wish. 

	The function can process dates from 1950 to 2049. Any input outside this range will yield "0.0". 

	This function supports DTG19 inputs in both "YY DDD HH MM SS.SSS" and "YYYYMonDDHHMMSS.SSS" formats. 

	:param str dtg: A string representation of time in DTG format
	:return:
		**ds50utc** (*float*) - Time as a python float, value in DTG20 format
	"""
	# Note: No maximum string size was specified by the chm docs, but based on DTG20 we know that limit is 22 characters
	# TODO: Add strict limit of 22 characters to dtg
	dtg = dtg.encode('ascii')
	if len(dtg) > 22:
		raise Exception("timedll.DTGToUTC(dtg) requires that dtg be ascii compatible string of 22 or fewer characters")
	ds50utc = C_TIMEDLL.DTGToUTC(dtg)
	if ds50utc == 0.0:
		raise Exception("timedll.DTGToUTC() returned a value of 0.0, which indicates an invalid or out of range input dtg")
	return ds50utc
	
## Get6P
# TODO: Figure out how to set argtypes when passing by reference
# C_TIMEDLL.Get6P.argtypes = [c.c_int, c.c_int, c.c_double, c.c_double, c.c_double]
C_TIMEDLL.Get6P.argtypes = [c.POINTER(c.c_int), c.POINTER(c.c_int), c.POINTER(c.c_double), c.POINTER(c.c_double), c.POINTER(c.c_double)]
def Get6P():
	"""
	Returns prediction control parameters.

	:return:
		- **startFrEpoch** (*int*) - Indicates whether startTime is expressed in minutes or days since Epoch. If startFrEpoch == 1, then startTime is in minutes since epoch. If startFrEpoch == 0, then startTime is in days since 1950, UTC.
		- **stopFrEpoch** (*int*) - Indicates whether stopTime is expressed in minutes or days since Epoch. If stopFrEpoch == 1, then stopTime is in minutes since epoch. If stopFrEpoch == 0, then stopTime is in days since 1950, UTC.
		- **startTime** (*float*) - The start time. Depending on the value of startFrEpoch, start time can be expressed in minutes since epoch or days since 1950, UTC.
		- **stopTime** (*float*) - The stop time. Depending on the value of stopFrEpoch, stop time can be expressed in minutes since epoch or days since 1950, UTC.
		- **interval** (*float*) - The step size (minutes).
	"""
	# initialize return variables
	startFrEpoch = c.c_int(0)
	stopFrEpoch = c.c_int(0)
	startTime = c.c_double(0)
	stopTime = c.c_double(0)
	stepSize = c.c_double(0)
	# fill return variables
	#C_TIMEDLL.Get6P(startFrEpoch, stopFrEpoch, startTime, stopTime, stepSize)
	C_TIMEDLL.Get6P(c.byref(startFrEpoch), c.byref(stopFrEpoch), c.byref(startTime), c.byref(stopTime), c.byref(stepSize))
	# replace with python equivalents
	startFrEpoch = startFrEpoch.value
	stopFrEpoch = stopFrEpoch.value
	startTime = startTime.value
	stopTime = stopTime.value
	stepSize = stepSize.value
	# return this data to the user
	return (startFrEpoch, stopFrEpoch, startTime, stopTime, stepSize)

## Get6PCardLine
C_TIMEDLL.Get6PCardLine.argtypes = [c.c_char_p]
def Get6PCardLine():
	"""
	Returns current prediction control parameters in the form of a 6P-Card string
	
	:return:
		**card6PLine** (*str*) - String representation of prediction control parameters.
	"""
	card6PLine = c.c_char_p(bytes(512))
	C_TIMEDLL.Get6PCardLine(card6PLine)
	card6PLine = settings.byte_to_str(card6PLine)
	return card6PLine
   

## IsTConFileLoaded
C_TIMEDLL.IsTConFileLoaded.restype = c.c_int
def IsTConFileLoaded():
	"""
	Checks to see if timing constants have been loaded into memory
	
	..Note:: the integer return type is preserved because I suspect SAA is using undocumented reason codes

	:return:
		-**load_status** (*int*) - 1 if timing constants are loaded, another value if not.
	"""
	load_status = C_TIMEDLL.IsTConFileLoaded()
	return load_status

## Set6P
C_TIMEDLL.Set6P.argtypes = [c.c_int, c.c_int, c.c_double, c.c_double, c.c_double]
def Set6P(startFrEpoch, stopFrEpoch, startTime, stopTime, stepSize):
	"""
	Set the prediction control parameters
	
	..Note:: SAA documentation uses the words "interval" and "stepSize" interchangeably
	
	:param int startFrEpoch: Indicates whether startTime is expressed in minutes since epoch.(startFrEpoch = 1: Value of startTime is in minutes since epoch, startFrEpoch = 0: Value of startTime is in days since 1950, UTC)
	:param int stopFrEpoch: Indicates whether stopTime is expressed in minutes since epoch. (stopFrEpoch = 1: Value of stopTime is in minutes since epoch, stopFrEpoch = 0: Value of stopTime is in days since 1950, UTC)
	:param float startTime: The start time. Depending on the value of startFrEpoch, start time can be expressed in minutes since epoch or days since 1950, UTC.
	:param float stopTime: The stop time. Depending on the value of stopFrEpoch, stop time can be expressed in minutes since epoch or days since 1950, UTC.
	:param float stepSize: The step size (minutes).
"""
	startFrEpoch = c.c_int(startFrEpoch)
	stopFrEpoch = c.c_int(stopFrEpoch)
	startTime = c.c_double(startTime)
	stopTime = c.c_double(stopTime)
	stepSize = c.c_double(stepSize)
	# TODO: Add value checking
	C_TIMEDLL.Set6P(startFrEpoch, stopFrEpoch, startTime, stopTime, stepSize)

## TAIToUT1
C_TIMEDLL.TAIToUT1.restype = c.c_double
C_TIMEDLL.TAIToUT1.argtypes = [c.c_double]
def TAIToUT1(ds50TAI):
	"""
	Converts a time in ds50TAI to a time in ds50UT1 using timing constants records in memory. If no timing constants records were loaded, ds50TAI and ds50UT1 are the same. 
	
	:param float ds50TAI: Days since 1950, TAI to be converted.
	:return:
		**ds50UT1** (*float*) - The number of days since 1950, UT1. Partial days will be represented as decimal days.
	"""
	ds50UT1 = C_TIMEDLL.TAIToUT1(ds50TAI)
	return ds50UT1

## TAIToUTC
C_TIMEDLL.TAIToUTC.restype = c.c_double
C_TIMEDLL.TAIToUTC.argtypes = [c.c_double]
def TAIToUTC(ds50TAI):
	"""
	Converts a time in ds50TAI to a time in ds50UTC using timing constants records in memory. If no timing constants records were loaded, ds50TAI and ds50UTC are the same. 

	:param float ds50TAI: Days since 1950, TAI to be converted.
	:return:
		**ds50UTC** (*float*) - The number of Days since 1950, UTC. Partial days may be returned.
	"""
	ds50UTC = C_TIMEDLL.TAIToUTC(ds50TAI)
	return ds50UTC

## TConAddARec
C_TIMEDLL.TConAddARec.restype = c.c_int
C_TIMEDLL.TConAddARec.argtypes = [c.c_double] * 7
def TConAddARec(refDs50UTC, leapDs50UTC, taiMinusUTC, ut1MinusUTC, ut1Rate, polarX, polarY):
	"""
	Adds a timing constant record to memory. Note that this function is solely for backward compatible with legacy software. The users should use TConLoadFile or TimeFuncLoadFile to load timing constants file instead. 
	
	:param float refDs50UTC: Reference time (days since 1950, UTC)
	:param float leapDs50UTC: Leap Second time (days since 1950, UTC)
	:param float taiMinusUTC: TAI minus UTC offset at the reference time (seconds)
	:param float ut1MinusUTC: UT1 minus UTC offset at the reference time (seconds)
	:param float ut1Rate: UT1 rate of change versus UTC at the reference time (msec/day)
	:param float polarX: Polar wander (X direction) at the reference time (arc-seconds)
	:param float polarY: Polar wander (Y direction) at the reference time (arc-seconds)
	:return:
		**retcode** (*int*) - 0 if timing constants are added to memory, !0 if there is an error.
	"""
	retcode = C_TIMEDLL.TConAddARec(refDs50UTC, leapDs50UTC, taiMinusUTC, ut1MinusUTC, ut1Rate, polarX, polarY)
	return retcode
	
## TConAddOne
C_TIMEDLL.TConAddOne.restype = c.c_int
C_TIMEDLL.TConAddOne.argtypes = [c.c_double] * 7
def TConAddOne(refDs50UTC, leapDs50UTC, taiMinusUTC, ut1MinusUTC, ut1Rate, polarX, polarY):
	"""
	Adds one timing constant record to memory. This API can be used to avoid TConLoadFile's file I/O 
	
	:param float refDs50UTC: Reference time (days since 1950, UTC)
	:param float leapDs50UTC: Leap Second time (days since 1950, UTC)
	:param float taiMinusUTC: TAI minus UTC offset at the reference time (seconds)
	:param float ut1MinusUTC: UT1 minus UTC offset at the reference time (seconds)
	:param float ut1Rate: UT1 rate of change versus UTC at the reference time (msec/day)
	:param float polarX: Polar wander (X direction) at the reference time (arc-seconds)
	:param float polarY: Polar wander (Y direction) at the reference time (arc-seconds)
	:return:
		**retcode** (*int*) - 0 if timing constants are added to memory, !0 if there is an error.
	"""
	retcode = C_TIMEDLL.TConAddOne(refDs50UTC, leapDs50UTC, taiMinusUTC, ut1MinusUTC, ut1Rate, polarX, polarY)
	return retcode


## TConLoadFile
C_TIMEDLL.TConLoadFile.restype = c.c_int
C_TIMEDLL.TConLoadFile.argtypes = [c.c_char_p]
def TConLoadFile(tconfile):
	"""

	Loads timing constants data from an input file. Time constants can be included directly in the main input file or they can be read from a separate file identified with "TIMFIL=[pathname/filename]". The input file is read in two passes. The function first looks for "TIMFIL=" lines, then it looks for timing constant data which was included directly. The result of this is that data entered using both methods will be processed, but the "TIMFIL=" data will be processed first. The time constants are also read in from each VCM. However, only the most recent time constants among VCMs are stored in the memory, see VCM.dll documentation. See the "Time Constants Data Description" section in the accompanying TimeFunc documentation file for supported formats.
	
	:param str tconfile: The name of the time constant file to load
	:return:
		**retcode** (*int*) - 0 if file successfully loaded, nonzero if file not successfully loaded
		
	"""
	tconfile = tconfile.encode('ascii')
	tconfile = settings.enforce_limit(tconfile, 512)
	tconfile = c.c_char_p(tconfile)
	retcode = C_TIMEDLL.TConLoadFile(tconfile)
	return retcode

## TConRemoveAll
C_TIMEDLL.TConRemoveAll.restype = c.c_int
def TConRemoveAll():
	"""
	Removes all the timing constants records in memory.
	
	:return:
		**retcode** (*int*) - 0 if all timing constants records are successfully removed from memory, non-0 if there is an error.
	"""
	retcode = C_TIMEDLL.TConRemoveAll()
	return retcode

## TConSaveFile
C_TIMEDLL.TConSaveFile.restype = c.c_int
C_TIMEDLL.TConSaveFile.argtypes = [c.c_char_p, c.c_int, c.c_int]
def TConSaveFile(tconfile, saveMode, saveForm):
	"""
	Saves currently loaded timing constants data to a file.

	TODO: Determine if XML format has been implemented.
	
	:param str tconfile: The name of the file in which to save the timing constants data, 512 character limit
	:param int saveMode: Specifies whether to create a new file or append to an existing one. (0 = Create new file, 1= Append to existing file)
	:param int saveForm: Specifies the format in which to save the file. (0 = SPECTER Print Record format, 1 = XML format (future implementation))
	:return:
		**retcode** (*int*) - 0 if the data is successfully saved to the file, non-0 if there is an error.
	"""
	tconfile = tconfile.encode('ascii')
	tconfile = settings.enforce_limit(tconfile, 512)
	tconfile = c.c_char_p(tconfile)
	saveMode = c.c_int(saveMode)
	saveForm = c.c_int(saveForm)
	retcode = C_TIMEDLL.TConSaveFile(tconfile, saveMode, saveForm)
	return retcode
	
## ThetaGrnwch
C_TIMEDLL.ThetaGrnwch.restype = c.c_double
C_TIMEDLL.ThetaGrnwch.argtypes = [c.c_double, settings.stay_int64]
def ThetaGrnwch(ds50UT1, envFk):
	"""
	Computes right ascension of Greenwich at the specified time in ds50UT1. The Fk constants as you currently have them set up in EnvConst.dll are used.

	:param float ds50UT1: Input days since 1950, UT1.
	:param stay_int64 envFk: A handle to the FK data. Use the value returned from envdll.EnvGetFkPtr()
	:return:
		**thetaGrnwhch** (*float*) - Right ascension of Greenwich in radians at the specified time.
	"""
	ds50UT1 = c.c_double(ds50UT1)
	envFK = settings.stay_int64(envFk)
	thetaGrnwhch = C_TIMEDLL.ThetaGrnwch(ds50UT1, envFk)
	return thetaGrnwhch	
	
## ThetaGrnwchFK4
C_TIMEDLL.ThetaGrnwchFK4.restype = c.c_double
C_TIMEDLL.ThetaGrnwchFK4.argtypes = [c.c_double]
def ThetaGrnwchFK4(ds50UT1):
	"""
	python:function:: ThetaGrnwchFK4
	Computes right ascension of Greenwich at the specified time in ds50UT1 using the Fourth Fundamental Catalogue (FK4). There is no need to load or initialize EnvConst.dll when computing right ascension using this function. 
	:param float ds50UT1: Input days since 1950, UT1.
	:return float thetaGrnwhchFK4: Right ascension of Greenwich in radians at the specified time using FK4.
	"""
	ds50UT1 = c.c_double(ds50UT1)
	thetaGrnwchcFK4 = C_TIMEDLL.ThetaGrnwchFK4(ds50UT1)
	return thetaGrnwchcFK4

## ThetaGrnwchFK5
C_TIMEDLL.ThetaGrnwchFK5.restype = c.c_double
C_TIMEDLL.ThetaGrnwchFK5.argtypes = [c.c_double]
def ThetaGrnwchFK5(ds50UT1):
	"""
	python:function:: ThetaGrnwchFK5
	Computes right ascension of Greenwich at the specified time in ds50UT1 using the Fifth Fundamental Catalogue (FK5). There is no need to load or initialize EnvConst.dll when computing right ascension using this function. 
	:param float ds50UT1: Input days since 1950, UT1.
	:return double thetaGrnwhchFK5: Right ascension of Greenwich in radians at the specified time using FK5.
	"""
	ds50UT1 = c.c_double(ds50UT1)
	thetaGrnwchcFK5 = C_TIMEDLL.ThetaGrnwchFK5(ds50UT1)
	return thetaGrnwchcFK5

## TimeComps1ToUTC
C_TIMEDLL.TimeComps1ToUTC.restype = c.c_double
C_TIMEDLL.TimeComps1ToUTC.argtypes = [c.c_int, c.c_int, c.c_int, c.c_int, c.c_double]
def TimeComps1ToUTC(year, dayOfYear, hh, mm, sss):
	"""
	python:function:: TimeComps1ToUTC
	Converts a set of time components (year, day of year, hour, minute, second) to a time in ds50UTC. Partial days may be returned. See "timedll.TimeComps2ToUTC" for a function which takes a month and day instead of a day of year value. 
	:param int year: The year time component. Either a four digit or two digit year is accepted.
	:param int dayOfYear: The day of the year
	:param int hh: The hour of the day
	:param int mm: The minute of the day
	:param float sss:  The second, including decimal seconds if desired
	"""
	year = c.c_int(year)
	dayOfYear = c.c_int(dayOfYear)
	hh = c.c_int(hh)
	mm = c.c_int(mm)
	sss = c.c_double(sss)
	ds50UTC = C_TIMEDLL.TimeComps1ToUTC(year, dayOfYear, hh, mm, sss)
	return ds50UTC

## TimeComps2ToUTC
C_TIMEDLL.TimeComps2ToUTC.restype = c.c_double
C_TIMEDLL.TimeComps2ToUTC.argtypes = [c.c_int, c.c_int, c.c_int, c.c_int, c.c_int, c.c_double]
def TimeComps2ToUTC(year, mon, dayOfMonth, hh, mm, sss):
	"""
	python:function:: TimeComps2ToUTC
	Converts a set of time components (year, month, day of month, hour, minute, second) to a time in ds50UTC. Partial days may be returned. See "TimeComps1ToUTC" for a function which takes a day of year value instead of a month and day. 
	:param int year: The year time component. Either a four digit or two digit year is accepted.
	:param int mon: the month as a number 1-12
	:param int dayOfMonth: The day of the month
	:param int hh: The hour of the day
	:param int mm: The minute of the day
	:param float sss:  The second, including decimal seconds if desired
	"""
	year = c.c_int(year)
	mon = c.c_int(mon)
	dayOfMonth = c.c_int(dayOfMonth)
	hh = c.c_int(hh)
	mm = c.c_int(mm)
	sss = c.c_double(sss)
	ds50UTC = C_TIMEDLL.TimeComps2ToUTC(year, mon, dayOfMonth, hh, mm, sss)
	return ds50UTC

## TimeConvFrTo
unknown_type = c.c_double * 512
#C_TIMEDLL.TimeConvFrTo.argtypes = [c.c_int, c.c_double, unknown_type]
C_TIMEDLL.TimeConvFrTo.argtypes = [c.c_int, unknown_type, unknown_type]
def TimeConvFrTo(funcIdx, frArr, toArr):
	"""
	python:function:: TimeConvFrTo
	This function is intended for future use. No information is currently available. 
	Developer note: because the interface has documented types, we "did our best"
	The documentation incorrectly identifies the frArr data type to be a double instead of a double[]. No big deal.
	It is unclear what the maximum array length is permitted to be. 
	It is not memory safe to use this function until we constrain the index lengths.
	:param int funcIdx: ?
	:param int frArr: ?
	:param int toArr: ?
	"""
	funcIdx = c.c_int(funcIdx)
	frArr_compatible = unknown_type()
	toArr_compatible = unknown_type()
	frArr_compatible = settings.feed_list_into_array(frArr, frArr_compatible)
	toArr_compatible = settings.feed_list_into_array(toArr, toArr_compatible)
	C_TIMEDLL.TimeConvFrTo(funcIdx, frArr_compatible, toArr_compatible)


## TimeFuncGetInfo
C_TIMEDLL.TimeFuncGetInfo.argtypes = [c.c_char_p]
def TimeFuncGetInfo():
	"""
	python:function:: TimeFuncGetInfo
	Returns the information about the TimeFunc DLL. 
	:returns str infoStr: up to 128 characters describing TimeFunc DLL
	"""
	infoStr = c.c_char_p(bytes(128))
	C_TIMEDLL.TimeFuncGetInfo(infoStr)
	infoStr = settings.byte_to_str(infoStr)
	return infoStr

## TimeFuncInit
C_TIMEDLL.TimeFuncInit.restype = c.c_int64
C_TIMEDLL.TimeFuncInit.argtypes = [c.c_int64]
def TimeFuncInit(maindll_handle):
	"""
	python:function:: TimeFuncInit
	Initializes a TimeFuncDLL object attached to the MainDLL object specified by maindll_handle pointer
	:param c.c_int64 maindll_handle: an integer pointer to the location of maindll in memory, returned by maindll.DllMainInit()
	:return int timedll_retcode: 0 on success, !0 on failure
	"""
	timedll_retcode = C_TIMEDLL.TimeFuncInit(maindll_handle)
	return timedll_retcode

## TimeFuncLoadFile
C_TIMEDLL.TimeFuncLoadFile.restype = c.c_int
C_TIMEDLL.TimeFuncLoadFile.argtypes = [c.c_char_p]
def TimeFuncLoadFile(tconfile):
	"""
	Loads timing constants data and prediction control (6P-card) from an input file. Time constants can be included directly in the main input file or they can be read from a separate file identified with "TIMFIL=[pathname/filename]". The input file is read in two passes. The function first looks for "TIMFIL=" lines, then it looks for timing constant data which was included directly. The result of this is that data entered using both methods will be processed, but the "TIMFIL=" data will be processed first. The time constants are also read in from each VCM. However, only the most recent time constants among VCMs are stored in the memory, see VCM.dll documentation.
	
	:param str tconfile: the location of the timing constants and prediction control file
	:return int retcode: 0 if input file loaded successfully, !0 otherwise
	"""
	tconfile = tconfile.encode('ascii')
	tconfile = settings.enforce_limit(tconfile, 512)
	tconfile = c.c_char_p(tconfile)
	retcode = C_TIMEDLL.TimeFuncLoadFile(tconfile)
	return retcode


## UTCToDTG15
C_TIMEDLL.UTCToDTG15.restype = c.c_char_p
C_TIMEDLL.UTCToDTG15.argtypes = [c.c_double, c.c_char_p]
def UTCToDTG15(ds50UTC):
	"""
	python:function:: UTCToDTG15
	Converts a ds50UTC time value (numeric double representing time since some epoch, need to locate citable docs) to a string of the form "YYDDDHHMMSS.SSS"
	:param int ds50UTC: time since epoch
	:return str dtg15: string representation of time
	"""
	if ds50UTC < 2192.0:
		raise Exception("ds50UTC must be greater than 2192.0, which cooresponds to Jan 1 1956.")
	dtg15 = c.c_char_p(bytes(15))
	C_TIMEDLL.UTCToDTG15(ds50UTC, dtg15)
	dtg15 = settings.byte_to_str(dtg15)
	return dtg15


## UTCToDTG17
C_TIMEDLL.UTCToDTG17.restype = c.c_char_p
C_TIMEDLL.UTCToDTG17.argtypes = [c.c_double, c.c_char_p]
def UTCToDTG17(ds50UTC):
	"""
	python:function:: UTCToDTG17
	Converts a ds50UTC time value (numeric double representing time since some epoch, need to locate citable docs) to a string of the form "YYYY/DDD.DDDDDDDD"
	:param int ds50UTC: time since epoch
	:return str dtg17: string representation of time
	"""
	if ds50UTC < 2192.0:
		raise Exception("ds50UTC must be greater than 2192.0, which cooresponds to Jan 1 1956.")
	dtg17 = c.c_char_p(bytes(17))
	C_TIMEDLL.UTCToDTG17(ds50UTC, dtg17)
	dtg17 = settings.byte_to_str(dtg17)
	return dtg17



## UTCToDTG19
C_TIMEDLL.UTCToDTG19.restype = c.c_char_p
C_TIMEDLL.UTCToDTG19.argtypes = [c.c_double, c.c_char_p]
def UTCToDTG19(ds50UTC):
	"""
	python:function:: UTCToDTG19
	Converts a ds50UTC time value (numeric double representing time since some epoch, need to locate citable docs) to a string of the form "YYYYMonDDHHMMSS.SSS"
	:param int ds50UTC: time since epoch
	:return str dtg19: string representation of time
	"""
	if ds50UTC < 2192.0:
		raise Exception("ds50UTC must be greater than 2192.0, which cooresponds to Jan 1 1956.")
	raise Exception("raw.timedll.UTCToDTG19(ds50UTC) function is disabled until I can figure out why C_TIMEDLL.UTCToDTG19(ds50UTC,dtg19) is causing a core dump")
	dtg19 = c.c_char_p(bytes(19))
	C_TIMEDLL.UTCToDTG19(ds50UTC, dtg19)
	dtg19 = settings.byte_to_str(dtg19)
	return dtg19



## UTCToDTG20
C_TIMEDLL.UTCToDTG20.restype = c.c_char_p
C_TIMEDLL.UTCToDTG20.argtypes = [c.c_double, c.c_char_p]
def UTCToDTG20(ds50UTC):
	"""
	python:function:: UTCToDTG20
	Converts a ds50UTC time value (numeric double representing time since some epoch, need to locate citable docs) to a string of the form "YYYY/DDD HHMM SS.SSS"
	:param int ds50UTC: time since epoch
	:return str dtg20: string representation of time
	"""
	if ds50UTC < 2192.0:
		raise Exception("ds50UTC must be greater than 2192.0, which cooresponds to Jan 1 1956.")
	dtg20 = c.c_char_p(bytes(20))
	C_TIMEDLL.UTCToDTG20(ds50UTC, dtg20)
	dtg20 = settings.byte_to_str(dtg20)
	return dtg20

## UTCToET
C_TIMEDLL.UTCToET.restype = c.c_double
C_TIMEDLL.UTCToET.argtypes = [c.c_double]
def UTCToET(ds50UTC):
	"""
	python:function::UTCToET
	Converts a time in ds50UTC to a time in ds50ET using timing constants records in memory. If no timing constants records were loaded, ds50UTC and ds50UT1 are the same. 
	:param float ds50UTC: Days since 1950, UTC to be converted.
	:return double ds50ET: The number of days since 1950, ET. Partial days may be returned.
	"""
	ds50UTC = c.c_double(ds50UTC)
	ds50ET = C_TIMEDLL.UTCToET(ds50UTC)
	return ds50ET

## UTCToTAI
C_TIMEDLL.UTCToTAI.restype = c.c_double
C_TIMEDLL.UTCToTAI.argtypes = [c.c_double]
def UTCToTAI(ds50UTC):
	"""
	python:function::UTCToTAI
	Converts a time in ds50UTC to a time in ds50TAI using timing constants records in memory. If no timing constants records were loaded, ds50UTC and ds50TAI are the same. 
	:param float ds50UTC: Days since 1950, UTC to be converted.
	:return double ds50TAI: The number of days since 1950, TAI. Partial days may be returned.
	"""
	ds50UTC = c.c_double(ds50UTC)
	ds50TAI = C_TIMEDLL.UTCToTAI(ds50UTC)
	return ds50TAI

## UTCToTConRec
C_TIMEDLL.UTCToTConRec.argtypes = [c.c_double] + [c.POINTER(c.c_double)] * 5
def UTCToTConRec(ds50UTC):
	"""
	python:function::UTCToTConRec
	Retrieves the timing constants record, if exists, at the requested input time in ds50UTC. If the requested record is not found, 0's will be returned for all of the constants. You can use this fact to determine whether the record was found or not. Simply check the taiMinusUTC value after calling this function. Since that value can never be 0 for a valid record, if it is 0 the record was not found. 
	:param float ds50UTC: Input days since 1950, UTC
	:return float taiMinusUTC: Returned TAI minus UTC offset at requested time (seconds)
	:return float ut1MinusUTC: Returned UT1 minus UTC offset at requested time (seconds)
	:return float ut1Rate: Returned UT1 rate of change versus UTC at Reference time (msec/day)
	:return float polarX: Returned interpolated polar wander (X direction) at requested time (arc-seconds)
	:return float polarY: Returned interpolated polar wander (Y direction) at requested time (arc-seconds)
	"""
	taiMinusUTC = c.c_double()
	ut1MinusUTC = c.c_double()
	ut1Rate = c.c_double()
	polarX = c.c_double()
	polarY = c.c_double()
	C_TIMEDLL.UTCToTConRec(ds50UTC, c.byref(taiMinusUTC), c.byref(ut1MinusUTC), c.byref(ut1Rate), c.byref(polarX), c.byref(polarY))
	taiMinusUTC = taiMinusUTC.value
	ut1MinusUTC = ut1MinusUTC.value
	ut1Rate = ut1Rate.value
	polarX = polarX.value
	polarY = polarY.value
	return (taiMinusUTC, ut1MinusUTC, ut1Rate, polarX, polarY)

## UTCToTimeComps1
C_TIMEDLL.UTCToTimeComps1.argtypes = [c.c_double] + [c.POINTER(c.c_int)] * 4 + [c.POINTER(c.c_double)]
def UTCToTimeComps1(ds50UTC):
	"""
	python:function::UTCToTimeComps1
	"""
	ds50UTC = c.c_double(ds50UTC)
	year = c.c_int()
	dayOfYear = c.c_int()
	hh = c.c_int()
	mm = c.c_int()
	sss = c.c_double()
	C_TIMEDLL.UTCToTimeComps1(ds50UTC, c.byref(year), c.byref(dayOfYear), c.byref(hh), c.byref(mm), c.byref(sss))
	year = year.value
	dayOfYear = dayOfYear.value
	hh = hh.value
	mm = mm.value
	sss = sss.value
	return (year, dayOfYear, hh, mm, sss)

## UTCToTimeComps2
C_TIMEDLL.UTCToTimeComps2.argtypes = [c.c_double] + [c.POINTER(c.c_int)] * 5 + [c.POINTER(c.c_double)]
def UTCToTimeComps2(ds50UTC):
	"""
	python:function::UTCToTimeCOmps2
	"""
	ds50UTC = c.c_double(ds50UTC)
	year = c.c_int()
	month = c.c_int()
	dayOfMonth = c.c_int()
	hh = c.c_int()
	mm = c.c_int()
	sss = c.c_double()
	C_TIMEDLL.UTCToTimeComps2(ds50UTC, c.byref(year), c.byref(month), c.byref(dayOfMonth), c.byref(hh), c.byref(mm), c.byref(sss))
	year = year.value
	month = month.value
	dayOfMonth = dayOfMonth.value
	hh = hh.value
	mm = mm.value
	sss = sss.value
	return(year, month, dayOfMonth, hh, mm, sss)

## UTCToUT1
C_TIMEDLL.UTCToUT1.restype = c.c_double
C_TIMEDLL.UTCToUT1.argtypes = [c.c_double]
def UTCToUT1(ds50UTC):
	"""
	python:function::UTCToUT1
	"""
	ds50UTC = c.c_double(ds50UTC)
	ds50UT1 = C_TIMEDLL.UTCToUT1(ds50UTC)
	return ds50UT1

## UTCToYrDays
C_TIMEDLL.UTCToYrDays.argtypes = [c.c_double, c.POINTER(c.c_int), c.POINTER(c.c_double)]
def UTCToYrDays(ds50UTC):
	"""
	python:function::UTCToYrDays
	"""
	ds50UTC = c.c_double(ds50UTC)
	year = c.c_int()
	dayOfYear = c.c_double()
	C_TIMEDLL.UTCToYrDays(ds50UTC, c.byref(year), c.byref(dayOfYear))
	year = year.value
	dayOfYear = dayOfYear.value
	return (year, dayOfYear)

## YrDaysToUTC
C_TIMEDLL.YrDaysToUTC.restype = c.c_double
C_TIMEDLL.YrDaysToUTC.argtypes = [c.c_int, c.c_double]
def YrDaysToUTC(year, dayOfYear):
	"""
	python:function::YrDaysToUTC
	"""
	year = c.c_int(year)
	dayOfYear = c.c_double(dayOfYear)
	ds50UTC = C_TIMEDLL.YrDaysToUTC(year, dayOfYear)
	return ds50UTC
