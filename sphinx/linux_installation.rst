.. toctree::
	:maxdepth: 2
	:caption: Contents:


Installing on Linux (Ubuntu 19.10)
==================================

Get the SAA DLLs
----------------

You must be a US citizen to lawfully download the SAA DLLs.

Go to `space-track.org <https://www.space-track.org/>`_, make an account, then go to the `sgp4 download page <https://www.space-track.org/documentation#/sgp4>`_ and download the appropriate package for your operating system. For me, this is ``SGP4_small_V7.9_LINUX64.tar.gz``. You should *also* download the windows package, ``SGP4_small_V7.9_WIN64.zip``, because the Windows package provides driver examples not present in the Linux version.

Verify the Python3 Environment
------------------------------

Check your Python3 version and make sure you are running at 3.7.5 or greater.

.. code-block:: bash

	$ python3 -V
	Python 3.7.5

Check your ctypes version and make sure you are running 1.1.0 or greater.

.. code-block:: bash

	$ python3 -c "import ctypes; print(ctypes.__version__)"
	1.1.0

Clone the ``dshsaa`` repository
-------------------------------

Clone the dshsaa repository to your working environment.

.. code-block:: bash

	$ cd ~
	$ git clone https://github.com/hardingprofessional/dshsaa.git

You should now have a folder called ``dshsaa`` on your current path.

Place the DLL/SO files in the libdll directory
----------------------------------------------

Untar your copy of ``SGP4_small_V7.9_LINUX64.tar.gz``. Navigate to ``SGP4_small_V7.9_LINUX64.tar.gz/Lib`` and copy all of the contents to ``~/dshsaa/dshsaa/libdll/``.

Install dependencies with pip3
------------------------------

If you don't have ``pip`` installed, install it.

.. code-block:: bash

	$ sudo apt update
	$ sudo apt install python3-pip
	$ sudo apt install python3-venv

Establish a virtual environment.

.. code-block:: bash

	$ cd ~/dshsaa
	$ python3 -m venv virtenv

You should now have a folder at ~/dshsaa/virtenv. Next, activate the virtual environment and install dependencies.

.. code-block:: bash

	$ source virtenv/bin/activate
	$ pip3 install --upgrade pip
	$ pip3 install -r requirements.txt

Sourcing virtenv/bin/activate fundamentally alters the python environment in the shell, and those changes will persist until the user executes the shell function deactivate. Your $PS1 shell prompt should indicate this by prepending (virtenv) to itself.


Set path and run tests
----------------------

Add the libdll to ``LD_LIBRARY_PATH``. This must be done any time the dshsaa module is used.

.. code-block:: bash

	$ cd ~/dshsaa
	$ source source_env

Run the full test battery

.. code-block:: bash

	$ ./runtest

The end of the output should look similar to this:

.. code-block:: bash
	
	...
	test_TleUpdateSatFrFieldsSP (raw.test_tledll.TestTleDll) ... ok
	testl_TleFieldsToSatKey (raw.test_tledll.TestTleDll) ... ok
	testl_TleFieldsToSatKeyML (raw.test_tledll.TestTleDll) ... skipped 'Segmentation fault, matlab'

	----------------------------------------------------------------------
	Ran 155 tests in 0.014s

	OK (skipped=14)

Test ability to build the documentation
---------------------------------------

Build the documentation with sphinx.

.. code-block:: bash

	$ cd ~/dshsaa/sphinx
	$ ./rebuild

Open the documentation by pointing your browser at ``~/dshsaa/sphinx/_build/html/index.html``.

Startup Notes
=============

Any time you run the module, you should do so from ``~/dshsaa`` and you must source ``source_env``. If you develop a program that uses this module, you should manually integrate the DLLs/SOs into your operating system and the python modules into your project.

Any time you build the docs, you must do so from ``~/dshsaa/sphinx`` using the ``./rebuild`` script.

I am investigating ways to fix these path dependencies.

Run ``dshsaa/example.py`` to make sure it works. Use this code as a reference until the sphinx documentation is improved.
