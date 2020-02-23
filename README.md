# `dshsaa`

## What Is it?

Airforce Space Command (AFSPC) distributes a copy of the binaries they use to compute the Standard Astrodynamic Algorithms (SAA) in Dynamic Link Library (DLL) form. To exactly replicate AFSPCs simulation results, one must use these DLLs to propogate orbits.

`dshsaa` is a python3 driver which allows the user to interface with the SAA DLLs using simple python3 code.

## Who should use this?

If you need to coordinate with AFSPC and want to get _exactly the same results_ AFSPC gets, use `dshsaa` and the SAA DLLs to propogate your orbits.

If you only wish to implement the SGP4 satellite tracking algorithms, use the `python-sgp4` package developed by Brandon Rhodes which is located [here](https://github.com/brandon-rhodes/python-sgp4). The deviation between Brandon's implementation and AFPSC's implementation is relatively small.

## Who made this?

David Harding built this driver to go with his blog at [blog.hardinglabs.com](https://blog.hardinglabs.com/python-ctypes-to-sgp4.html).

## TODO (Non-Code)

1. Test on Windows
2. Test on MacOS (Catalina drops 32bit support, may not work)

## TODO (Code, but not core functionality)
<ol> <li> Add a test environment validation script that verifies </li> 
	<ol type="a">
		<li> dll path is known and populated </li>
		<li> python version is accurate </li>
		<li> ctypes version is acceptable </li>
		<li> dependencies are available </li>
	</ol>
</ol>

## Installation

Installation on Linux is fully tested on Ubuntu 16.04 and 18.04. Installation on Windows and MacOS is still in development.

## Linux

### Get the SAA DLLs

You must be a US citizen to lawfully download the SAA DLLs.

Go to [space-track.org](https://www.space-track.org/), make an account, then go to the [sgp4 download page](https://www.space-track.org/documentation#/sgp4) and download the appropriate package for your operating system. For me, this is `SGP4_small_V7.9_LINUX64.tar.gz`. You should _also_ download the windows package, `SGP4_small_V7.9_WIN64.zip`, because the Windows package provides driver examples not present in the Linux version.

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

### Install dependencies with `pip3`

If you don't have pip installed, install it.

```
$ sudo apt update
$ sudo apt install python3-pip
```

Establish a virtual environment.

```
$ cd ~/dshsaa
$ python3 -m venv virtenv
```

You should now have a folder at ~/dshsaa/virtenv. Next, activate the virtual environment and install dependencies.

```
$ source virtenv/bin/activate
$ pip3 install --upgrade pip
$ pip3 install -r requirements.txt
```

> Sourcing `virtenv/bin/activate` fundamentally alters the python environment in the shell, and those changes will persist until the user executes the shell function `deactivate`. Your `$PS1` shell prompt should indicate this by prepending `(virtenv)` to itself.

### Set path and run tests

Add the libdll to `LD_LIBRARY_PATH`. This must be done any time the `dshsaa` module is used.

```
$ cd ~/dshsaa
$ source source_env
```

Run the full test battery

```
$ ./runtest
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

# Test ability to build the documentation

Build the documentation with sphinx.

```
$ cd ~/dshsaa/sphinx
$ ./rebuild
```

Open the documentation by pointing your browser at `~/dshsaa/sphinx/_build/html/index.html`.

# Starting Notes

Any time you run the module, you should do so from `~/dshsaa` and you must `source source_env`. 

Any time you build the docs, you must do so from `~/dshsaa/sphinx` using the `./rebuild` script. 

I am investigating ways to fix this.

Run `dshsaa/example.py` to make sure it works. Use this code as a reference until the sphinx documentation is improved.


