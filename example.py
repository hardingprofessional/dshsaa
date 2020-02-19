#! /user/bin/env python3

"""
This script is intended to demonstrate how to use the raw SGP4 interface to perform a common task: propogate an orbit.
The simplest possible syntax is used to assist new developers.
"""

# Import settings. This module configures some environment variables and shared assets.
from dshsaa.raw import settings

# Import all the dll interfaces. These modules provide direct access to the various dlls.
from dshsaa.raw import maindll, envdll, astrodll, timedll, tledll, sgp4dll

#init maindll and the other components of the SGP4 package
maindll_handle = maindll.DllMainInit()

# open a log file
maindll.OpenLogFile('example.log')

# init the other DLLs
retcode = timedll.TimeFuncInit(maindll_handle)
if retcode != 0:
		raise Exception("Failed to init %s with error code %i" % ('timedll', retcode))
	
retcode = tledll.TleInit(maindll_handle)
if retcode != 0:
		raise Exception("Failed to init %s with error code %i" % ('tledll', retcode))
	
retcode = envdll.EnvInit(maindll_handle)
if retcode != 0:
		raise Exception("Failed to init %s with error code %i" % ('envdll', retcode))
	
retcode = astrodll.AstroFuncInit(maindll_handle)
if retcode != 0:
		raise Exception("Failed to init %s with error code %i" % ('astrodll', retcode))
	
sgp4dll.Sgp4SetLicFilePath('./dshsaa/libdll/') #get the license before initing sgp4
retcode = sgp4dll.Sgp4Init(maindll_handle)
if retcode != 0:
		raise Exception("Failed to init %s with error code %i" % ('sgp4dll', retcode))
	
# Initialize a TLE
line1 = '1 90001U SGP4-VAL 93 51.47568104  .00000184      0 0  00000-4   814'
line2 = '2 90001   0.0221 182.4922 0000720  45.6036 131.8822  1.00271328 1199'
satKey = tledll.TleAddSatFrLines(line1, line2)
if satKey.value <= 0:
	raise Exception("Failed to init satKey with code %i" % satKey.value)

# Initialize that satellite in the SGP4 context
retcode = sgp4dll.Sgp4InitSat(satKey)
if retcode != 0:
	raise Exception("Failed to init tle with code %i" % (retcode))

# Propogate the orbit 3600 seconds
(retcode, ds50UTC, pos, vel, llh) = sgp4dll.Sgp4PropMse(satKey, 2700)

print("retcode:  %i" % (retcode))
print("ds50UTC:  {:13.7f}".format(ds50UTC))
print("position: < {:13.7f}, {:14.7f}, {:14.7f} >".format(pos[0], pos[1], pos[2]))
print("velocity: < {:13.7f}, {:14.7f}, {:14.7f} >".format(vel[0], vel[1], vel[2]))

