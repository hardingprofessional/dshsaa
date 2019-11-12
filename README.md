# dshsaa

## WARNING: THIS CODE IS IN EARLY DEVELOPMENT, DO NOT USE IN PRODUCTION

## What Is it?

Airforce Space Command (AFSPC) distributes a copy of the code they use that implements the Standard Astrodynamic Algorithms (SAA) in Dynamic Link Library (DLL) form. To exactly replicate AFSPCs simulation results, one must use these DLLs to propogate orbits.

`dshsaa` is a python3 driver which allows the user to interface with the SAA DLLs using simple python3 code.

## Who should use this?

If you need to coordinate with AFSPC and want to get _exactly the same results_ AFSPC is getting, use `dshsaa` and the SAA DLLs to propogate your orbits.

If you only wish to implement the SGP4 satellite tracking algorithms, use the `python-sgp4` package developed by Brandon Rhodes which is located [here](https://github.com/brandon-rhodes/python-sgp4). The deviation between Brandon's implementation and AFPSC's implementation is relatively small.

## Who made this?

David Harding built this driver to go with his blog at [blog.hardinglabs.com](https://blog.hardinglabs.com/python-ctypes-to-sgp4.html).
