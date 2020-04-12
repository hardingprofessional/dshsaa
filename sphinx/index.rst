.. dshsaa documentation master file, created by
   sphinx-quickstart on Thu Feb 20 12:34:09 2020.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. toctree::
	:maxdepth: 2
	:caption: Contents:
	
dshsaa
======

This is the homepage for documenation regarding the `dshsaa python module <https://github.com/hardingprofessional/dshsaa>`_.

What is dshsaa?
===============

Airforce Space Command (AFSPC) distributes a copy of the binaries they use to compute the Standard Astrodynamic Algorithms (SAA) in Dynamic Link Library (DLL) form. To exactly replicate AFSPCs simulation results, one must use these DLLs to propogate orbits.

dshsaa is a python3 driver which allows the user to interface with the SAA DLLs using simple python3 code.

Who should use this?
====================

If you need to coordinate with AFSPC and want to get exactly the same results AFSPC gets, use dshsaa and the SAA DLLs to propogate your orbits.

If you only wish to implement the SGP4 satellite tracking algorithms, use the python-sgp4 package developed by Brandon Rhodes which is located `here <https://github.com/brandon-rhodes/python-sgp4>`_. The deviation between Brandon's implementation and AFPSC's implementation is relatively small.

Who made this?
==============

David Harding built this driver to go with his blog at `blog.hardinglabs.com <https://blog.hardinglabs.com>`_.

TODO List (Non-Code)
====================

#. Test on Windows
#. Test on MacOS

TODO List (Code)
================

#. Create a test environment validation script that:

	#. verifies DLL/SO path is known and populated
	#. Verifies python version is adequate
	#. Verifies ctypes version is acceptable
	#. Verifies dependencies in requirements.txt are installed, or prompts to install them

Installation
============

Installation instructions for MacOS and Windows are in development.

Installation guides are listed here:

* `Linux Installation (Ubuntu 19.10) <./linux_installation.html>`_

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
