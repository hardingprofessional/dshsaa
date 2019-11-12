#! /usr/bin/env python3

"""
exceptions.py contains all custom warnings and exceptions for the package
"""

class Error(Exception):
	"""Base class for other exceptions"""
	pass

class KnownFault(Error):
	"""Raised when known bad code would be run"""
	pass
	
