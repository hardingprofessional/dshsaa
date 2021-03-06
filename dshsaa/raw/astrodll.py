#! /usr/bin/env python3

import dshsaa.raw.settings as settings
import dshsaa.raw.exceptions as exceptions
import ctypes as c
import pdb

C_ASTRODLL = c.CDLL(settings.LIB_ASTRO_NAME)

##AstroConvFrTo 
C_ASTRODLL.AstroConvFrTo.argtypes = [c.c_int, settings.double128, settings.double128]
def AstroConvFrTo(xf_Conv, frArr):
	"""
	This function is intended for future use. No information is currently available.

	Because the purpose of frArr and toArr is unclear, each array is automatically set to the maximum length permitted in the C_ASTRODLL spec.

	:param int xf_Conv: The purpose of this parameter is not yet known

	:param float[<=128] frArr: The purpose of this parameter is not yet known

	:return: 
		**toArr** (*float[128]*) - The output array of data
	"""
	xf_Conv = c.c_int(xf_Conv)
	frArr_compatible = settings.double128()
	toArr_compatible = settings.double128()
	frArr_compatible = settings.feed_list_into_array(frArr, frArr_compatible)
	C_ASTRODLL.AstroConvFrTo(xf_Conv, frArr_compatible, toArr_compatible)
	toArr = settings.array_to_list(toArr_compatible)
	return toArr

##AstroFuncGetInfo 
C_ASTRODLL.AstroFuncGetInfo.argtypes = [c.c_char_p]
def AstroFuncGetInfo():
	"""
	Retrieves information about the current version of AstroFunc.dll.

	:return:
		**infoStr** (*str*) - A string describing version number, build date, and platform
	"""
	infoStr = c.c_char_p(bytes(128))
	C_ASTRODLL.AstroFuncGetInfo(infoStr)
	infoStr = settings.byte_to_str(infoStr)
	return infoStr

##AstroFuncInit
C_ASTRODLL.AstroFuncInit.restype = c.c_int
C_ASTRODLL.AstroFuncInit.argtypes = [settings.stay_int64]
def AstroFuncInit(maindll_handle):
	"""
	Initializes AstroFunc DLL for use in the program.

	If this function returns an error, it is recommended that you stop the program immediately. 

	An error will occur if you forget to load and initialize all the prerequisite DLLs, as listed in the DLL Prerequisites section of the accompanying documentation, before using this DLL. 

	:param settings.stay_int64 maindll_handle: The handle that was reaturned by maindll.DllMainInit()

	:return:
		**retcode** (*int*) - 0 if AstroFunc.dll is initialized successfully, non-0 if there is an error.
"""
	retcode = C_ASTRODLL.AstroFuncInit(maindll_handle)
	return retcode

##AToN
C_ASTRODLL.AToN.restype = c.c_double
C_ASTRODLL.AToN.argtypes = [c.c_double]
def AToN(a):
	"""
	Converts semi-major axis A to mean motion N. 

	:param float a: Semi-major axis A (km).

	:return: 
		**N** (*float*) - The mean motion N (revs/day).
	"""
	a = c.c_double(a)
	N = C_ASTRODLL.AToN(a)
	return N

##AzElToLAD
C_ASTRODLL.AzElToLAD.argtypes = [c.c_double, c.c_double, settings.double3, settings.double3, settings.double3]
def AzElToLAD(az, el):
	"""
	Converts azimuth and elevation to vector triad LAD in topocentric horizontal coordinate system. 

	:param float az: Input azimuth (deg).
	:param float el: Input elevation angle (deg).
	:return:
		- **Lh** (*float[3]*) - The resulting unit vector from the station to the satellite (referred to the horizon coordinate system axis). (double[3])
		- **Ah** (*float[3]*) - The resulting unit vector perpendicular to the hour circle passing through the satellite, in the direction of increasing Az. (double[3])
		- **Dh** (*float[3]*) - The resulting unit vector perpendicular to L and is directed toward the zenith, in the plane of the hour circle. (double[3])
"""
	az = c.c_double(az)
	el = c.c_double(el)
	Lh = settings.double3()
	Ah = settings.double3()
	Dh = settings.double3()
	C_ASTRODLL.AzElToLAD(az, el, Lh, Ah, Dh)
	Lh = settings.array_to_list(Lh)
	Ah = settings.array_to_list(Ah)
	Dh = settings.array_to_list(Dh)
	return (Lh, Ah, Dh)

##AzElToRaDec
C_ASTRODLL.AzElToRaDec.argtypes = [c.c_double] * 4 + [c.POINTER(c.c_double)] * 2
def AzElToRaDec(thetaG, lat, lon, az, el):
	"""
	Converts Azimuth/Elevation in local horizon reference frame to Right Ascension/Declination in topocentric reference frame. Requires some information about the ground site.
	
	:param float thataG: greenwhich mean sidereal time (rad)
	:param float lat: station's astronomical latitude (deg, +N, -S)
	:param float lon: station's astronomical longitude (deg, +E, -W)
	:param float az: station's azimuth (deg)
	:param float el: station's elevation (deg)
	:return:
		- **RA** (*float*) - station's right ascension (deg)
		- **dec** (*float*) - station's declination (deg)
	"""
	thetaG = c.c_double(thetaG)
	lat = c.c_double(lat)
	lon = c.c_double(lon)
	az = c.c_double(az)
	el = c.c_double(el)
	RA = c.c_double()
	dec = c.c_double()
	C_ASTRODLL.AzElToRaDec(thetaG, lat, lon, az, el, c.byref(RA), c.byref(dec))
	return (RA, dec)

##BrouwerToKozai 
C_ASTRODLL.BrouwerToKozai.restype = c.c_double
C_ASTRODLL.BrouwerToKozai.argtypes = [c.c_double] * 3
def BrouwerToKozai(eccen, incli, nBrouwer):
	"""
	Converts Brouwer mean motion to Kozai mean motion. 

	:param float eccen: eccentricity
	:param float incli: inclination (degrees)
	:param float nBrouwer: Brouwer mean motion (revs/day).
	:return:
		**kozai** (*float*) - Kozai mean motion (revs/day).
	"""
	eccen = c.c_double(eccen)
	incli = c.c_double(incli)
	nBrouwer = c.c_double(nBrouwer)
	kozai = C_ASTRODLL.BrouwerToKozai(eccen, incli, nBrouwer)
	return kozai

##ClassToEqnx
C_ASTRODLL.ClassToEqnx.argtypes = [settings.double6] * 2
def ClassToEqnx(metricClass):
	"""
	Converts a set of classical elements to a set of equinoctial elements. 

	:param float[6] metricClass: The set of classical elements to be converted. (double[6])
	:return: 
		**metricEqnx** (*float[6]*) - The resulting set of equinoctial elements. (double[6])
	"""
	metricClass_compatible = settings.double6()
	metricEqnx_compatible = settings.double6()
	metricClass_compatible = feed_list_into_array(metricClass)
	C_ASTRODLL.ClassToEqnx(metricClass_compatible, metricEqnx_compatible)
	metricEqnx = settings.array_to_list(metricEqnx_compatible)
	return(metricEqnx)

##CompMoonPos 
C_ASTRODLL.CompMoonPos.argtypes = [c.c_double, settings.double3, c.POINTER(c.c_double)]
def CompMoonPos(ds50ET):
	"""
	Computes the Moon position at the specified time. 

	:param float ds50ET: The number of days since 1950, ET for which to compute the moon position.
	:return:
		- **uvecMoon** (*float[3]*) - The resulting moon position unit vector. (double[3])
		- **moonVecMag** (*float*) - The resulting magnitude of the moon position vector (km).
	"""
	ds50ET = c.c_double(ds50ET)
	uvecMoon = settings.double3()
	moonVecMag = c.c_double()
	C_ASTRODLL.CompMoonPos(ds50ET, uvecMoon, c.byref(moonVecMag))
	uvecMoon = settings.array_to_list(uvecMoon)
	moonVecMag = moonVecMag.value
	return(uvecMoon, moonVecMag)

##CompSunMoonPos 
C_ASTRODLL.CompSunMoonPos.argtypes = [c.c_double, settings.double3, c.POINTER(c.c_double), settings.double3, c.POINTER(c.c_double)]
def CompSunMoonPos(ds50ET):
	"""
	Computes the Sun and Moon position at the specified time. 
	
	:param float ds50ET: The number of days since 1950, ET for which to compute the sun and moon position.
	:return:
		- **uvecSun** (*float[3]*) - The resulting sun position unit vector. (double[3])
		- **sunVecMag** (*float*) - The resulting magnitude of the sun position vector (km).
		- **uvecMoon** (*float[3]*) - The resulting moon position unit vector. (double[3])
		- **moonVecMag** (*float*) - The resulting magnitude of the moon position vector (km).
	"""
	ds50ET = c.c_double(ds50ET)
	uvecSun = settings.double3()
	sunVecMag = c.c_double()
	uvecMoon = settings.double3()
	moonVecMag = c.c_double()
	C_ASTRODLL.CompSunMoonPos(ds50ET, uvecSun, c.byref(sunVecMag), uvecMoon, c.byref(moonVecMag))
	uvecSun = settings.array_to_list(uvecSun)
	sunVecMag = sunVecMag.value
	uvecMoon = settings.array_to_list(uvecMoon)
	moonVecMag = moonVecMag.value
	return (uvecSun, sunVecMag, uvecMoon, moonVecMag)

##CompSunPos
C_ASTRODLL.CompSunPos.argtypes = [c.c_double, settings.double3, c.POINTER(c.c_double)]
def CompSunPos(ds50ET):
	"""
	Computes the Sun position at the specified time. 
	
	:param float ds50ET: The number of days since 1950, ET for which to compute the sun position.
	:return:
		- **uvecSun** (*float[3]*) - The resulting sun position unit vector. (double[3])
		- **sunVecMag** (*float*) - The resulting magnitude of the sun position vector (km).
	"""
	ds50ET = c.c_double(ds50ET)
	uvecSun = settings.double3()
	sunVecMag = c.c_double()
	C_ASTRODLL.CompSunPos(ds50ET, uvecSun, c.byref(sunVecMag))
	uvecSun = settings.array_to_list(uvecSun)
	sunVecMag = sunVecMag.value
	return (uvecSun, sunVecMag)

##CompTrueAnomaly 
C_ASTRODLL.CompTrueAnomaly.restype = c.c_double
C_ASTRODLL.CompTrueAnomaly.argtypes = [settings.double6]
def CompTrueAnomaly(metricKep):
	"""
	Computes true anomaly from a set of Keplerian elements. 

	:param float[6] metricKep: The set of Keplerian elements for which to compute true anomaly. (double[6])
	:return:
		**true_anomaly** (*float*) - The true anomaly in degrees.
	"""
	metricKep = settings.list_to_array(metricKep)
	true_anomaly = C_ASTRODLL.CompTrueAnomaly(metricKep)
	return true_anomaly
	
##CovMtxPTWToUVW
C_ASTRODLL.CovMtxPTWToUVW.argtypes = [settings.double3, settings.double3, settings.double6x6, settings.double6x6]
def CovMtxPTWToUVW(pos, vel, ptwCovMtx):
	"""
	Converts covariance matrix PTW to UVW. 
	
	:param float[3] pos: The input position vector (km). (double[3])
	:param float[3] vel: The input velocity vector (km/s). (double[3])
	:param float[6][6] ptwCovMtx: The PTW covariance matrix to be converted. (double[6,6])
	:return:
		**uvwCovMtx** (*float[6][6]*) - The resulting UVW covariance matrix. (double[6,6])
	"""
	# initialize ctypes
	pos_compatible = settings.double3()
	vel_compatible = settings.double3()
	ptwCovMtx_compatible = settings.double6x6()
	uvwCovMtx_compatible = settings.double6x6()
	# copy list data into ctypes
	pos_compatible = settings.feed_list_into_array(pos, pos_compatible)
	vel_compatible = settings.feed_list_into_array(vel, vel_compatible)
	ptwCovMtx_compatible = settings.feed_2d_list_into_array(ptwCovMtx, ptwCovMtx_compatible)
	# call DLL, will fill uvwCovMtx_compatible
	C_ASTRODLL.CovMtxPTWToUVW(pos_compatible, vel_compatible, ptwCovMtx_compatible, uvwCovMtx_compatible)
	# convert to python datatype and confirm
	uvwCovMtx = settings.array2d_to_list(uvwCovMtx_compatible)
	return uvwCovMtx

##CovMtxUVWToPTW
C_ASTRODLL.CovMtxUVWToPTW.argtypes = [settings.double3, settings.double3, settings.double6x6, settings.double6x6]
def CovMtxUVWToPTW(pos, vel, uvwCovMtx):
	"""
	Converts covariance matrix UVW to PTW

	:param float[3] pos: the input position vector (km) (double[3])
	:param float[3] vel: the input velocity vector (km/s) (double[3])
	:param float[6][6] uvwCovMtx: the UVW covariance matrix to be converted. (double[6,6])
	:return:
		**ptwCovMtx** (*float[6][6]*) - The resulting PTW covariance matrix (double[6,6])
	"""
	# initialize ctypes
	# initialize ctypes
	pos_compatible = settings.double3()
	vel_compatible = settings.double3()
	ptwCovMtx_compatible = settings.double6x6()
	uvwCovMtx_compatible = settings.double6x6()
	# copy list data into ctypes
	pos_compatible = settings.feed_list_into_array(pos, pos_compatible)
	vel_compatible = settings.feed_list_into_array(vel, vel_compatible)
	uvwCovMtx_compatible = settings.feed_2d_list_into_array(uvwCovMtx, ptwCovMtx_compatible)
	# call DLL, will fill ptwCovMtx_compatible
	C_ASTRODLL.CovMtxPTWToUVW(pos_compatible, vel_compatible, uvwCovMtx_compatible, ptwCovMtx_compatible)
	# convert to python datatype and return
	ptwCovMtx = settings.array2d_to_list(uvwCovMtx_compatible)
	return ptwCovMtx
	
##EarthObstructionAngles 
C_ASTRODLL.EarthObstructionAngles.argtypes = [c.c_double, settings.double3, settings.double3, c.POINTER(c.c_double), c.POINTER(c.c_double), c.POINTER(c.c_double)]
def EarthObstructionAngles(earthLimb, satECI, senECI):
	"""
	Computes Earth/Sensor/Earth Limb and Earth/Sensor/Satellite angles.
	
	:param float earthLimb: Earth limb distance (km).
	:param float[3] satECI: Satellite position in ECI (km). (double[3])
	:param float[3] senECI: Sensor position in ECI (km). (double[3])
	:return:
		- **earthSenLimb** (*float*) - The resulting earth/sensor/limb angle (deg).
		- **earthSenSat** (*float*) - The resulting earth/sensor/sat angle (deg).
		- **satEarthSen** (*float*) - The resulting sat/earth/sensor angle (deg).
	"""
	earthLimb = c.c_double(earthLimb)
	satECI_compatible = settings.double3()
	senECI_compatible = settings.double3()
	earthSenLimb = c.c_double()
	earthSenSat = c.c_double()
	satEarthSen = c.c_double()
	satECI_compatible = settings.feed_list_into_array(satECI, satECI_compatible)
	senECI_compatible = settings.feed_list_into_array(senECI, senECI_compatible)
	C_ASTRODLL.EarthObstructionAngles(earthLimb, satECI_compatible, senECI_compatible, c.byref(earthSenLimb), c.byref(earthSenSat), c.byref(satEarthSen))
	#pdb.set_trace()
	earthSenLimb = earthSenLimb.value
	earthSenSat = earthSenSat.value
	satEarthSen = satEarthSen.value
	return (earthSenLimb, earthSenSat, satEarthSen)

##ECIToEFG
C_ASTRODLL.ECIToEFG.argtypes = [c.c_double] + [settings.double3] * 4
def ECIToEFG(thetaG, posECI, velECI):
	"""
	Converts ECI position and velocity vectors to EFG position and velocity vectors. 
	
	:param float thetaG: Theta - Greenwich mean sidereal time (rad).
	:param float[3] posECI: The ECI (TEME of Date) position vector (km) to be converted. (double[3])
	:param float[3] velECI: The ECI (TEME of Date) velocity vector (km/s) to be converted. (double[3])
	:return:
		- **posEFG** (*float[3]*) - The resulting EFG position vector (km). (double[3])
		- **velEFG** (*float[3]*) - The resulting EFG velocity vector (km/s). (double[3])
	"""
	thetaG = c.c_double(thetaG)
	posECI = settings.list_to_array(posECI)
	velECI = settings.list_to_array(velECI)
	posEFG = settings.double3()
	velEFG = settings.double3()
	C_ASTRODLL.ECIToEFG(thetaG, posECI, velECI, posEFG, velEFG)
	posEFG = settings.array_to_list(posEFG)
	velEFG = settings.array_to_list(velEFG)
	return (posEFG, velEFG)

##ECIToTopoComps
C_ASTRODLL.ECIToTopoComps.argtypes = [c.c_double] * 2 + [settings.double3] * 3 + [settings.double10]
def ECIToTopoComps(theta, lat, senPos, satPos, satVel):
	"""
	Converts satellite ECI position/velocity vectors and sensor location to topocentric components.
	
	:param float theta: Theta - local sidereal time(rad).
	:param float lat: Station's astronomical latitude (deg). (+N) (-S)
	:param float[3] senPos: Sensor position in ECI (km). (double[3])
	:param float[3] satPos: Satellite position in ECI (km). (double[3])
	:param float[3] satVel: Satellite velocity in ECI (km/s). (double[3])
	:return:
		**xa_topo** (*float[10]*) - An array that stores the resulting topocentric components. (double[10])

			- [0]: Resulting right ascension (RA) (deg) 
			- [1]: Declination (deg) 
			- [2]: Azimuth (deg) 
			- [3]: Elevation (deg) 
			- [4]: Range (km) 
			- [5]: RAdot (first derivative of right ascension) (deg/s) 
			- [6]: DecDot (first derivative of declination) (deg/s) 
			- [7]: AzDot (first derivative of azimuth) (deg/s) 
			- [8]: ElDot (first derivative of elevation) (deg/s) 
			- [9]: RangeDot (first derivative of range) (km/s) 
	"""
	theta = c.c_double(theta)
	lat = c.c_double(lat)
	senPos = settings.list_to_array(senPos)
	satPos = settings.list_to_array(satPos)
	satVel = settings.list_to_array(satVel)
	xa_topo = settings.double10()
	C_ASTRODLL.ECIToTopoComps(theta, lat, senPos, satPos, satVel, xa_topo)
	xa_topo = settings.array_to_list(xa_topo)
	return xa_topo
	
##ECRToEFG
C_ASTRODLL.ECRToEFG.argtypes = [c.c_double] * 2 + [settings.double3] * 4
def ECRToEFG(polarX, polarY, posECR, velECR):
	"""
	Converts ECR position and velocity vectors to EFG position and velocity vectors.

	:param float polarX: Polar motion X (arc-sec).
	:param float polarY: Polar motion Y (arc-sec).
	:param float[3] posECR: The ECR position vector (km) to be converted. (double[3])
	:param float[3] velECR: The ECR velocity vector (km/s) to be converted. (double[3])
	:return:
		- **posEFG** (*float[3]*) - The resulting EFG position vector (km). (double[3])
		- **velEFG** (*float[3]*) -	The resulting EFG velocity vector (km/s). (double[3])
	"""
	polarX = c.c_double(polarX)
	polarY = c.c_double(polarY)
	posECR = settings.list_to_array(posECR)
	velECR = settings.list_to_array(velECR)
	posEFG = settings.double3()
	velEFG = settings.double3()
	C_ASTRODLL.ECRToEFG(polarX, polarY, posECR, velECR, posEFG, velEFG)
	posEFG = settings.array_to_list(posEFG)
	velEFG = settings.array_to_list(velEFG)
	return (posEFG, velEFG)
	
##EFGPosToLLH
C_ASTRODLL.EFGPosToLLH.argtypes = [settings.double3] * 2
def EFGPosToLLH(posEFG):
	"""
	Converts an EFG position vector to geodetic latitude, longitude, and height. 
	
	:param float[3] posEFG: The EFG position vector (km) to be converted. (double[3])
	:return:
		**metricLLH** (*float[3]*) - The resulting geodetic north latitude (degree), east longitude (degree), and height (km). (double[3])
	"""
	posEFG = settings.list_to_array(posEFG)
	metricLLH = settings.double3()
	C_ASTRODLL.EFGPosToLLH(posEFG, metricLLH)
	metricLLH = settings.array_to_list(metricLLH)
	return metricLLH
	
##EFGToECI
C_ASTRODLL.EFGToECI.argtypes = [c.c_double] + [settings.double3] * 3
def EFGToECI(thetaG, posEFG, velEFG):
	"""
	Converts EFG position and velocity vectors to ECI position and velocity vectors. 
	
	:param float thetaG: Theta - Greenwich mean sidereal time (rad).
	:param float[3] posEFG: The EFG position vector (km) to be converted. (double[3])
	:param float[3] velEFG: The EFG velocity vector (km/s) to be converted. (double[3])
	:return:
		- **posECI** (*float[3]*) - The resulting ECI (TEME of Date) position vector (km). (double[3])
		- **velECI** (*float[3]*) - The resulting ECI (TEME of Date) velocity vector (km/s). (double[3])
	"""
	thetaG = c.c_double(thetaG)
	posEFG = settings.list_to_array(posEFG)
	velEFG = settings.list_to_array(velEFG)
	posECI = settings.double3()
	velECI = settings.double3()
	C_ASTRODLL.EFGToECI(thetaG, posEFG, velEFG, posECI, velECI)
	posECI = settings.array_to_list(posECI)
	velECI = settings.array_to_list(velECI)
	return (posECI, velECI)
	
##EFGToECR
C_ASTRODLL.EFGToECR.argtypes = [c.c_double] * 2 + [settings.double3] * 4
def EFGToECR(polarX, polarY, posEFG, velEFG):
	"""
	Converts EFG position and velocity vectors to ECR position and velocity vectors.

	:param float polarX: Polar motion X (arc-sec).
	:param float polarY: Polar motion Y (arc-sec).
	:param float[3] posEFG: The EFG position vector (km) to be converted. (double[3])
	:param float[3] velEFG: The EFG velocity vector (km/s) to be converted. (double[3])
	:return:
		- **posECR** (*float[3]*) - The resulting ECR position vector (km). (double[3])
		- **velECR** (*float[3]*) - The resulting ECR velocity vector (km/s). (double[3])
	"""
	polarX = c.c_double(polarX)
	polarY = c.c_double(polarY)
	posEFG = settings.list_to_array(posEFG)
	velEFG = settings.list_to_array(velEFG)
	posECR = settings.double3()
	velECR = settings.double3()
	C_ASTRODLL.EFGToECR(polarX, polarY, posEFG, velEFG, posECR, velECR)
	posECR = settings.array_to_list(posECR)
	velECR = settings.array_to_list(velECR)
	return (posECR, velECR)	
	
##EqnxToClass 
C_ASTRODLL.EqnxToClass.argtypes = [settings.double6] * 2
def EqnxToClass(metricEqnx):
	"""
	Converts a set of equinoctial elements to a set of classical elements
	
	TODO: Determine and document vector sequence
	
	:param float[6] metricEqnx: The set of equinoctial elements to be converted. (double[6])
	:return:
		**metricClass** (*float[6]*) - The resulting set of classical elements. (double[6])
	"""
	metricEqnx = settings.list_to_array(metricEqnx)
	metricClass = settings.double6()
	C_ASTRODLL.EqnxToClass(metricEqnx, metricClass)
	metricClass = settings.array_to_list(metricClass)
	return metricClass

##EqnxToKep
C_ASTRODLL.EqnxToKep.argtypes = [settings.double6] * 2
def EqnxToKep(metricEqnx):
	"""
	Converts a set of equinoctial elements to a set of classical elements
	
	TODO: Determine and document vector sequence
	
	:param float[6] metricEqnx: The set of equinoctial elements to be converted. (double[6])
	:return:
		**metricClass** (*float[6]*) - The resulting set of classical elements. (double[6])
	"""
	metricEqnx = settings.list_to_array(metricEqnx)
	metricKep = settings.double6()
	C_ASTRODLL.EqnxToKep(metricEqnx, metricKep)
	metricKep = settings.array_to_list(metricKep)
	return metricKep

##EqnxToPosVel
C_ASTRODLL.EqnxToPosVel.argtypes = [settings.double6] + [settings.double3] * 2
def EqnxToPosVel(metricEqnx):
	"""
	Converts a set of equinoctial elements to position and velocity vectors. 
	
	:param float[6] metricEqnx: The set of equinoctial elements to be converted. (double[6])
	:return:
		- **pos** (*float[3]*) - The resulting position vector. (double[3])
		- **vel** (*float[3]*) - The resulting velocity vector. (double[3])
	"""
	metricEqnx = settings.list_to_array(metricEqnx)
	pos = settings.double3()
	vel = settings.double3()
	C_ASTRODLL.EqnxToPosVel(metricEqnx, pos, vel)
	pos = settings.array_to_list(pos)
	vel = settings.array_to_list(vel)
	return (pos, vel)

##GetInitialDrag
C_ASTRODLL.GetInitialDrag.argtypes = [c.c_double] * 2 + [c.POINTER(c.c_double)] * 2
def GetInitialDrag(semiMajorAxis, eccen):
	"""
	Computes initial values for the SGP drag term NDOT and the SGP4 drag term BSTAR based upon eccentricity and semi-major axis. 
	
	:param float semiMajorAxis: Semi-major axis (km).
	:param float eccen: Eccentricity (unitless).
	:return:
		- **ndot** (*float*) - Ndot (revs/day^2).
		- **bstar** (*float*) - Bstar (1/earth radii).
	"""
	semiMajorAxis = c.c_double(semiMajorAxis)
	eccen = c.c_double(eccen)
	ndot = c.c_double()
	bstar = c.c_double()
	C_ASTRODLL.GetInitialDrag(semiMajorAxis, eccen, c.byref(ndot), c.byref(bstar))
	ndot = ndot.value
	bstar = bstar.value
	return (ndot, bstar)

##IsPointSunlit
C_ASTRODLL.IsPointSunlit.argtypes = [c.c_double, settings.double3]
C_ASTRODLL.IsPointSunlit.restype = c.c_int
def IsPointSunlit(ds50ET, ptEci):
	"""
	Determines if a point in space is sunlit at the input time ds50ET 
	
	:param float ds50ET: The number of days since 1950, ET for which to determine if the point is sunlit.
	:param float ptEci: a position in ECI (km). (double[3])
	:return:
		**retcode** (*int*) - 0 if unlit, 1 if lit, possibly other values on error (undocumented)
	"""
	raise exceptions.KnownFault("IsPointSunlit method always returns 1, whether that is correct or not. This issue is under investigation but will not be resolved soon.")
	ds50ET = c.c_double(ds50ET)
	ptEci = settings.list_to_array(ptEci)
	retcode = C_ASTRODLL.IsPointSunlit(ds50ET, ptEci)
	return retcode

##KepOscToMean
C_ASTRODLL.KepOscToMean.argtypes = [settings.double6] * 2
def KepOscToMean(metricOscKep):
	"""
	Converts a set of osculating Keplerian elements to a set of mean Keplerian elements using method 9 algorithm. 
	
	:param float[6] metricOscKep: The set of osculating Keplerian elements to be converted. (double[6])
	:return:
		**metricMeanKep** (*float[6]*) - The resulting set of mean Keplerian elements. (double[6])
	"""
	metricOscKep = settings.list_to_array(metricOscKep)
	metricMeanKep = settings.double6()
	C_ASTRODLL.KepOscToMean(metricOscKep, metricMeanKep)
	metricMeanKep = settings.array_to_list(metricMeanKep)
	return metricMeanKep

##KepToEqnx 
C_ASTRODLL.KepToEqnx.argtypes = [settings.double6] * 2
def KepToEqnx(metricKep):
	"""
	Converts a set of Keplerian elements to a set of equinoctial elements. 
	
	:param float[6] metricKep: The set of Keplerian elements to be converted. (double[6])
	:return:
		**metricEqnx** (*float[6]*) - The resulting set of equinoctial elements. (double[6])
	"""
	metricKep = settings.list_to_array(metricKep)
	metricEqnx = settings.double6()
	C_ASTRODLL.KepToEqnx(metricKep, metricEqnx)
	metricEqnx = settings.array_to_list(metricEqnx)
	return metricEqnx

##KepToPosVel
C_ASTRODLL.KepToPosVel.argtypes = [settings.double6] + [settings.double3] * 2
def KepToPosVel(metricKep):
	"""
	Converts a set of osculating Keplerian elements to osculating position and velocity vectors. 
	
	:param float[6] metricKep: The set of Keplerian elements to be converted. (double[6])
	:return:
		- **pos** (*float[3]*) - The resulting position vector. (double[3])
		- **vel** (*float[3]*) - The resulting velocity vector. (double[3])
	"""
	metricKep = settings.list_to_array(metricKep)
	pos = settings.double3()
	vel = settings.double3()
	C_ASTRODLL.KepToPosVel(metricKep, pos, vel)
	pos = settings.array_to_list(pos)
	vel = settings.array_to_list(vel)
	return (pos, vel)

##KepToUVW
C_ASTRODLL.KepToUVW.argtypes = [settings.double6] + [settings.double3] * 3
def KepToUVW(metricKep):
	"""
	Converts a set of Keplerian elements to Ubar, Vbar, and Wbar vectors. 
	
	:param float[6] metricKep: The set of Keplerian elements to be converted. (double[6])
	:return:
		- **uBar** (*float[3]*) - The resulting ubar vector. (double[3])
		- **vBar** (*float[3]*) - The resulting vbar vector. (double[3])
		- **wBar** (*float[3]*) - The resulting wbar vector. (double[3])
	"""
	metricKep = settings.list_to_array(metricKep)
	uBar = settings.double3()
	vBar = settings.double3()
	wBar = settings.double3()
	C_ASTRODLL.KepToUVW(metricKep, uBar, vBar, wBar)
	uBar = settings.array_to_list(uBar)
	vBar = settings.array_to_list(vBar)
	wBar = settings.array_to_list(wBar)
	return (uBar, vBar, wBar)
	
##KozaiToBrouwer
C_ASTRODLL.KozaiToBrouwer.restype = c.c_double
C_ASTRODLL.KozaiToBrouwer.argtypes = [c.c_double, c.c_double, c.c_double]
def KozaiToBrouwer(eccen, incli, nKozai):
	"""
	Converts Kozai mean motion to Brouwer mean motion. 
	
	:param float eccen: eccentricity
	:param float incli: inclination (degrees)
	:param float nKozai: Kozai mean motion (revs/day).
	:return:
		**nBrouwer** (*float*) - Brouwer mean motion (revs/day).
	"""
	eccen = c.c_double(eccen)
	incli = c.c_double(incli)
	nKozai = c.c_double(nKozai)
	nBrouwer = C_ASTRODLL.KozaiToBrouwer(eccen, incli, nKozai)
	return nBrouwer
	
##LLHToEFGPos
C_ASTRODLL.LLHToEFGPos.argtypes = [settings.double3] * 2
def LLHToEFGPos(metricLLH):
	"""
	Converts geodetic latitude, longitude, and height to an EFG position vector.
	
	:param float[3] metricLLH: An Array containing the geodetic north latitude (degree), east longitude (degree), and height (km) to be converted. (double[3])
	:return:
		**posEFG** (*float[3]*) - The resulting EFG position vector (km). (double[3])
	"""
	metricLLH = settings.list_to_array(metricLLH)
	posEFG = settings.double3()
	C_ASTRODLL.LLHToEFGPos(metricLLH, posEFG)
	posEFG = settings.array_to_list(posEFG)
	return posEFG

##LLHToXYZ
C_ASTRODLL.LLHToXYZ.argtypes = [c.c_double] + [settings.double3] * 2
def LLHToXYZ(thetaG, metricLLH):
	"""
	Converts geodetic latitude, longitude, and height to an ECI position vector XYZ. 
	
	:param float thetaG: Theta - Greenwich mean sidereal time (rad).
	:param float[3] metric LLH: An array containing geodetic north latitude (degree), east longitude (degree), and height (km) to be converted. (double[3])
	:return:
		**metricXYZ** (*float[3]*) - The resulting ECI (TEME of Date) position vector (km). (double[3])
	"""
	thetaG = c.c_double(thetaG)
	metricLLH = settings.list_to_array(metricLLH)
	metricXYZ = settings.double3()
	C_ASTRODLL.LLHToXYZ(thetaG, metricLLH, metricXYZ)
	metricXYZ = settings.array_to_list(metricXYZ)
	return metricXYZ
	
##NToA
C_ASTRODLL.NToA.restype = c.c_double
C_ASTRODLL.NToA.argtypes = [c.c_double]
def NToA(n):
	"""
	Converts mean motion N to semi-major axis A. 
	
	:param float n: Mean motion N (revs/day).
	:return:
		**a** (*float*) - The semi-major axis A (km).
	"""
	n = c.c_double(n)
	a = C_ASTRODLL.NToA(n)
	return a


##PosVelMuToEqnx
C_ASTRODLL.PosVelMuToEqnx.argtypes = [settings.double3] * 2 + [c.c_double, settings.double6]
def PosVelMuToEqnx(pos, vel, mu):
	"""
	Converts position and velocity vectors to a set of equinoctial elements with the given mu value.
	
	:param float[3] pos: The position vector to be converted. (double[3])
	:param float[3] vel: The velocity vector to be converted. (double[3])
	:param float mu: The value of mu.
	:return:
		**metricEqnx** (*float[6]*) - The resulting set of equinoctial elements. (double[6])
	"""
	pos = settings.list_to_array(pos)
	vel = settings.list_to_array(vel)
	mu = c.c_double(mu)
	metricEqnx = settings.double6()
	C_ASTRODLL.PosVelMuToEqnx(pos, vel, mu, metricEqnx)
	metricEqnx = settings.array_to_list(metricEqnx)
	return metricEqnx

##PosVelMuToKep 
C_ASTRODLL.PosVelMuToKep.argtypes = [settings.double3] * 2 + [c.c_double, settings.double6]
def PosVelMuToKep(pos, vel, mu):
	"""
	Converts osculating position and velocity vectors to a set of osculating Keplerian elements with the given value of mu.
	
	:param float[3] pos: The position vector to be converted. (double[3])
	:param float[3] vel: The velocity vector to be converted. (double[3])
	:param float mu: The value of mu.
	:return:
		 **metricKep** (*float[6]*) - The resulting set of Keplerian elements. (double[6])
	"""
	pos = settings.list_to_array(pos)
	vel = settings.list_to_array(vel)
	mu = c.c_double(mu)
	metricKep = settings.double6()
	C_ASTRODLL.PosVelMuToKep(pos, vel, mu, metricKep)
	metricKep = settings.array_to_list(metricKep)
	return metricKep
	
##PosVelToEqnx
C_ASTRODLL.PosVelToEqnx.argtypes = [settings.double3] * 2 + [settings.double6]
def PosVelToEqnx(pos, vel):
	"""
	Converts position and velocity vectors to a set of equinoctial elements. 
	
	:param float[3] pos: The position vector to be converted. (double[3])
	:param float[3] vel: The velocity vector to be converted. (double[3])
	:return:
		 **metricEqnx** (*float[6]*) - The resulting set of equinoctial elements. (double[6])
	"""
	pos = settings.list_to_array(pos)
	vel = settings.list_to_array(vel)
	metricEqnx = settings.double6()
	C_ASTRODLL.PosVelToEqnx(pos, vel, metricEqnx)
	metricEqnx = settings.array_to_list(metricEqnx)
	return metricEqnx

##PosVelToKep
C_ASTRODLL.PosVelToKep.argtypes = [settings.double3] * 2 + [settings.double6]
def PosVelToKep(pos, vel):
	"""
	Converts osculating position and velocity vectors to a set of osculating Keplerian elements. 
	
	:param float[3] pos: The position vector to be converted. (double[3])
	:param float[3] vel: The velocity vector to be converted. (double[3])
	:return:
		**metricKep** (*float[6]*) - The resulting set of Keplerian elements. (double[6])
	"""
	pos = settings.list_to_array(pos)
	vel = settings.list_to_array(vel)
	metricKep = settings.double6()
	C_ASTRODLL.PosVelToKep(pos, vel, metricKep)
	metricKep = settings.array_to_list(metricKep)
	return metricKep	
	
##PosVelToPTW
C_ASTRODLL.PosVelToPTW.argtypes = [settings.double3] * 5
def PosVelToPTW(pos, vel):
	"""
	Converts position and velocity vectors to U, V, W vectors.
	The resulting vectors have the following meanings. 
	U vector: V x W 
	V vector: along velocity direction 
	W vector: pos x vel 
	
	:param float[3] pos: The position vector to be converted. (double[3])
	:param float[3] vel: The velocity vector to be converted. (double[3])
	:return:
		- **uVec** (*float[3]*) - The resulting U vector. (double[3])
		- **vVec** (*float[3]*) - The resulting V vector. (double[3])
		- **wVec** (*float[3]*) - The resulting W vector. (double[3])
	"""
	pos = settings.list_to_array(pos)
	vel = settings.list_to_array(vel)
	uVec = settings.double3()
	vVec = settings.double3()
	wVec = settings.double3()
	C_ASTRODLL.PosVelToPTW(pos, vel, uVec, vVec, wVec)
	uVec = settings.array_to_list(uVec)
	vVec = settings.array_to_list(vVec)
	wVec = settings.array_to_list(wVec)
	return (uVec, vVec, wVec)
	
##PosVelToUUVW
C_ASTRODLL.PosVelToUUVW.argtypes = [settings.double3] * 5
def PosVelToUUVW(pos, vel):
	"""
	Converts position and velocity vectors to U, V, W vectors. 
	The resulting vectors have the following meanings. 
	U vector: along radial direction 
	V vector: W x U 
	W vector: pos x vel 
	
	:param float[3] pos: The position vector to be converted. (double[3])
	:param float[3] vel: The velocity vector to be converted. (double[3])
		- **uVec** (*float[3]*) - The resulting U vector. (double[3])
		- **vVec** (*float[3]*) - The resulting V vector. (double[3])
		- **wVec** (*float[3]*) - The resulting W vector. (double[3])
	"""
	pos = settings.list_to_array(pos)
	vel = settings.list_to_array(vel)
	uVec = settings.double3()
	vVec = settings.double3()
	wVec = settings.double3()
	C_ASTRODLL.PosVelToUUVW(pos, vel, uVec, vVec, wVec)
	uVec = settings.array_to_list(uVec)
	vVec = settings.array_to_list(vVec)
	wVec = settings.array_to_list(wVec)
	return (uVec, vVec, wVec)

##RaDecToAzEl
C_ASTRODLL.RaDecToAzEl.argtypes = [c.c_double] * 5 + [c.POINTER(c.c_double)] * 2
def RaDecToAzEl(thetaG, lat, lon, RA, dec):
	"""
	Converts right ascension and declination in the topocentric reference frame to Azimuth/Elevation in the local horizon reference frame. 

	:param float thetaG: Theta - Greenwich mean sidereal time (rad).
	:param float lat: Station's astronomical latitude (deg). (+N) (-S)
	:param float lon: Station's astronomical longitude (deg). (+E) (-W)
	:param float RA: Right ascension (deg)
	:param float dec: Declination (deg)
	:return:
		- **az** (*float*) - Azimuth (deg)
		- **el** (*float*) - Elevation (deg)
	"""
	thetaG = c.c_double(thetaG)
	lat = c.c_double(lat)
	lon =  c.c_double(lon)
	RA = c.c_double(RA)
	dec = c.c_double(dec)
	az = c.c_double()
	el = c.c_double()
	C_ASTRODLL.RaDecToAzEl(thetaG, lat, lon, RA, dec, az, el)
	az = az.value
	el = el.value
	return (az, el)

##RADecToLAD
C_ASTRODLL.RADecToLAD.argtypes = [c.c_double] * 2 + [settings.double3] * 3
def RADecToLAD(RA, dec):
	"""
	Converts right ascension and declination to vector triad LAD in topocentric equatorial coordinate system. 
	
	:param float RA: Right ascension (deg)
	:param float dec: Declination (deg)
	:return:
		- **L** (*float[3]*) - The resulting unit vector from the station to the satellite (referred to the equatorial coordinate system axis). (double[3])
		- **A_Tilde** (*float[3]*) - The resulting unit vector perpendicular to the hour circle passing through the satellite, in the direction of increasing RA. (double[3])
		- **D_Tilde** (*float[3]*) - The resulting unit vector perpendicular to L and is directed toward the north, in the plane of the hour circle. (double[3])
	"""
	RA = c.c_double(RA)
	dec = c.c_double(dec)
	L = settings.double3()
	A_Tilde = settings.double3()
	D_Tilde = settings.double3()
	C_ASTRODLL.RADecToLAD(RA, dec, L, A_Tilde, D_Tilde)
	L = settings.array_to_list(L)
	A_Tilde = settings.array_to_list(A_Tilde)
	D_Tilde = settings.array_to_list(D_Tilde)
	return (L, A_Tilde, D_Tilde)

##RAEToECI
C_ASTRODLL.RAEToECI.argtypes = [c.c_double] * 2 + [settings.double6] + [settings.double3] * 3
def RAEToECI(theta, astroLat, xa_rae):
	"""
	Converts full state RAE (range, az, el, and their rates) to full state ECI (position and velocity)

	:param float theta: Theta - local sidereal time(rad).
	:param float astroLat: Astronomical latitude (ded).
	:param float[6] xa_rae: An array contains input data. The data at each index is listed below. (double[6])

		- [0]: Range (km) 
		- [1]: Azimuth (deg) 
		- [2]: Elevation (deg) 
		- [3]: Range Dot (km/s) 
		- [4]: Azimuth Dot (deg/s) 
		- [5]: Elevation Dot (deg/s) 
	
	:return:
		- **senPos** (*float[3]*) - Sensor position in ECI (km). (double[3])
		- **satPos** (*float[3]*) - Satellite position in ECI (km). (double[3])
		- **satVel** (*float[3]*) - Satellite velocity in ECI (km/s). (double[3])
	"""
	theta = c.c_double(theta)
	astroLat = c.c_double(astroLat)
	xa_rae = settings.list_to_array(xa_rae)
	senPos = settings.double3()
	satPos = settings.double3()
	satVel= settings.double3()
	C_ASTRODLL.RAEToECI(theta, astroLat, xa_rae, senPos, satPos, satVel)
	senPos = settings.array_to_list(senPos)
	satPos = settings.array_to_list(satPos)
	satVel = settings.array_to_list(satVel)
	return (senPos, satPos, satVel)

##RotDateToJ2K
C_ASTRODLL.RotDateToJ2K.argtypes = [c.c_int32] * 2 + [c.c_double] + [settings.double3] * 4
def RotDateToJ2K(spectr, nutationTerms, ds50TAI, posDate, velDate):
	"""
	Rotates position and velocity vectors from coordinates of date to J2000. 
	
	:param float spectr: Specifies whether to run in SPECTR compatibility mode. A value of 1 means Yes.
	:param float nutationTerms: Nutation terms (4-106, 4:less accurate, 106:most acurate).
	:param float ds50TAI: Time in days since 1950, TAI for which the coordinates of position and velocity vectors are currently expressed.
	:param float[3] posDate: The position vector from coordinates of Date. (double[3])
	:param float[3] velDate: The velocity vector from coordinates of Date. (double[3])
	:return:
		- **posJ2K** (*float[3]*) - The resulting position vector in coordinates of J2000. (double[3])
		- **velJ2K** (*float[3]*) - The resulting velocity vector in coordinates of J2000. (double[3])
	"""
	spectr = c.c_int32(spectr)
	nutationTerms = c.c_int32(nutationTerms)
	ds50TAI = c.c_double(ds50TAI)
	posDate = settings.list_to_array(posDate)
	velDate = settings.list_to_array(velDate)
	posJ2K = settings.double3()
	velJ2K = settings.double3()
	C_ASTRODLL.RotDateToJ2K(spectr, nutationTerms, ds50TAI, posDate, velDate, posJ2K, velJ2K)
	posJ2K = settings.array_to_list(posJ2K)
	velJ2K = settings.array_to_list(velJ2K)
	return (posJ2K, velJ2K)
	
##RotJ2KToDate
C_ASTRODLL.RotJ2KToDate.argtypes = [c.c_int32] * 2 + [c.c_double] + [settings.double3] * 4
def RotJ2KToDate(spectr, nutationTerms, ds50TAI, posDate, velDate):
	"""
	Rotates position and velocity vectors from coordinates of date to J2000. 
	
	:param float spectr: Specifies whether to run in SPECTR compatibility mode. A value of 1 means Yes.
	:param float nutationTerms: Nutation terms (4-106, 4:less accurate, 106:most acurate).
	:param float ds50TAI: Time in days since 1950, TAI for which the coordinates of position and velocity vectors are currently expressed.
	:param float[3] posJ2K: The position vector from J2000. (double[3])
	:param float[3] velJ2K: The velocity vector from J2000. (double[3])
	:return:
		- **posDate** (*float[3]*) - The resulting position vector in coordinates of date, ds50TAI. (double[3])
		- **velDate** (*float[3]*) - The resulting velocity vector in coordinates of date, ds50TAI. (double[3])
	"""
	spectr = c.c_int32(spectr)
	nutationTerms = c.c_int32(nutationTerms)
	ds50TAI = c.c_double(ds50TAI)
	posJ2K = settings.list_to_array(posJ2K)
	velJ2K = settings.list_to_array(velJ2K)
	posDate = settings.double3()
	velDate = settings.double3()
	C_ASTRODLL.RotJ2KToDate(spectr, nutationTerms, ds50TAI, posJ2K, velJ2K, posDate, velDate)
	posDate = settings.array_to_list(posDate)
	velDate = settings.array_to_list(velDate)
	return (posDate, velDate)

##SolveKepEqtn
C_ASTRODLL.SolveKepEqtn.restype = c.c_double
C_ASTRODLL.SolveKepEqtn.argtypes = [settings.double6]
def SolveKepEqtn(metricKep):
	"""
	Solves Kepler's equation (M = E - e sin(E)) for the eccentric anomaly, E, by iteration. 
	
	:param float[6] metricKep: The set of Keplerian elements for which to solve the equation. (double[6])
	:return:
		**E** (*float*) - The eccentric anomaly "E"
	"""
	metricKep = settings.list_to_array(metricKep)
	E = C_ASTRODLL.SolveKepEqtn(metricKep)
	return E

##XYZToLLH
C_ASTRODLL.XYZToLLH.argtypes = [c.c_double] + [settings.double3] * 2
def XYZToLLH(thetaG, metricPos):
	"""
	Converts an ECI position vector XYZ to geodetic latitude, longitude, and height. 
	
	:param float thetaG: ThetaG - Greenwich mean sidereal time (rad).
	:param float[3] metricPos: The ECI (TEME of Date) position vector (km) to be converted. (double[3])
	:return:
		**metricLLH** (*float[3]*) - The resulting geodetic north latitude (degree), east longitude(degree), and height (km). (double[3])
	"""
	thetaG = c.c_double(thetaG)
	metricPos = settings.list_to_array(metricPos)
	metricLLH = settings.double3()
	C_ASTRODLL.XYZToLLH(thetaG, metricPos, metricLLH)
	metricLLH = settings.array_to_list(metricLLH)
	return metricLLH
