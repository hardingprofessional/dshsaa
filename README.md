# `dshsaa`

## What Is it?

Airforce Space Command (AFSPC) distributes a copy of the code they use that implements the Standard Astrodynamic Algorithms (SAA) in Dynamic Link Library (DLL) form. To exactly replicate AFSPCs simulation results, one must use these DLLs to propogate orbits.

`dshsaa` is a python3 driver which allows the user to interface with the SAA DLLs using simple python3 code.

## Who should use this?

If you need to coordinate with AFSPC and want to get _exactly the same results_ AFSPC is getting, use `dshsaa` and the SAA DLLs to propogate your orbits.

If you only wish to implement the SGP4 satellite tracking algorithms, use the `python-sgp4` package developed by Brandon Rhodes which is located [here](https://github.com/brandon-rhodes/python-sgp4). The deviation between Brandon's implementation and AFPSC's implementation is relatively small.

## Who made this?

David Harding built this driver to go with his blog at [blog.hardinglabs.com](https://blog.hardinglabs.com/python-ctypes-to-sgp4.html).


## TODO (Non-Code)

1. Implement a properly defined virtual environment spec so others can test
2. Fix the Sphinx documentation component
3. Test on Windows
4. Test on MacOS (Catalina drops 32bit support, may not work)

## TODO (Code, but not core functionality)
1. Add a test environment validation script that verifies
	a. dll path is known and populated
	b. python version is accurate
	c. ctypes version is acceptable
	d. dependencies are available

## Installation

_These instructions will change when the Virtual Environment is completed._

## Linux

### Get the SAA DLLs

You must be a US citizen to lawfully download the SAA DLLs.

Go to [space-track.org](https://www.space-track.org/), make an account, then go to the [sgp4 download page](https://www.space-track.org/documentation#/sgp4) and download the appropriate package for your operating system. For me, this is `SGP4_small_V7.9_LINUX64.tar.gz`. You should _also_ download the windows package, `SGP4_small_V7.9_WIN64.zip`, because it provides additional Python2 driver examples.

### Verify Python3 Environment

Check your Python3 version and make sure you are running at 3.7.5 or greater.

```
$ python3 -V
Python 3.7.5
```

Check your ctypes version and make sure you are running 1.1.0 or greater.

```
python3 -c "import ctypes; print(ctypes.__version__)"
1.1.0
```

### Clone the `dshsaa` repository

Clone the `dshsaa` repository to your working environment. 

```
$ cd ~
$ git clone https://github.com/hardingprofessional/dshsaa.git
```

You should now have a folder called `dshsaa` on your current path.

### Place the DLL/SO files in the libdll directory

Untar your copy of `SGP4_small_V7.9_LINUX64.tar.gz`. Navigate to `SGP4_small_V7.9_LINUX64.tar.gz/Lib` and copy all of the contents to `~/dshsaa/dshsaa/libdll/`.

### Set path and run tests

Add the libdll to LD_LIBRARY_PATH.

```
$ cd ~/dshsaa
$ source source_env
```

Run the full test battery

```
./runtest
```

The end of the output should look similar to this:

```
...
test_TleUpdateSatFrFieldsSP (raw.test_tledll.TestTleDll) ... ok
testl_TleFieldsToSatKey (raw.test_tledll.TestTleDll) ... ok
testl_TleFieldsToSatKeyML (raw.test_tledll.TestTleDll) ... skipped 'Segmentation fault, matlab'

----------------------------------------------------------------------
Ran 155 tests in 0.014s

OK (skipped=14)
```


