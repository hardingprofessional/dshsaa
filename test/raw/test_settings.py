#! /usr/bin/env python3
import unittest
from dshsaa.raw import settings
import pdb
import ctypes as c

class TestSettings(unittest.TestCase):
	def setUp(self):
		return None
	
	def test_list_to_array(self):
		li1 = [1.1, 2.2, 3.3]
		ar1 = settings.list_to_array(li1)
		li2 = [1, 2, 3]
		ar2 = settings.list_to_array(li2, c.c_int)
	
	def test_str_to_byte(self):
		s = "dog"
		b1 = settings.str_to_byte(s)
		b2 = settings.str_to_byte(s, fixed_width = 10)
		b3 = settings.str_to_byte(s, limit = 5)
		b4 = settings.str_to_byte(s, terminator = settings.string_term)
		self.assertEqual(b1, b'dog')
		self.assertEqual(b2, b'dog\x00\x00\x00\x00\x00\x00\x00')
		self.assertEqual(b3, b'dog')
		self.assertEqual(b4, b'dog\x00')
		# TODO: Add tests to make sure errors are thrown when memory conditions are violated
	
	def test_str_to_c_char_p(self):
		s = "dog"
		c1 = settings.str_to_c_char_p(s)
		c2 = settings.str_to_c_char_p(s, fixed_width = 10)
		c3 = settings.str_to_c_char_p(s, limit = 5)
		c4 = settings.str_to_c_char_p(s, terminator = settings.string_term)
		
		
	def test_array2d_to_list(self):
		ar_t = (c.c_double * 3) * 3
		ar = ar_t()
		li_inp = [[0.0, 0.1, 0.2], [1.0, 1.1, 1.2], [2.0, 2.1, 2.2]]
		settings.feed_2d_list_into_array(li_inp, ar)
		li_out = settings.array2d_to_list(ar)
		
	
	def tearDown(self):
		return None
