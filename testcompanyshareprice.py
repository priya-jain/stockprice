#This is a test file which unit test the method getMaxShare1 and getMaxShare2 of the module priyajain_codingexercise.

#To run this file we need priyajain_codingexercise.py to be present at the same location.

import unittest
import sys
from priyajain_codingexercise import CompanyStock, InvalidFile

class TestCompanySharePrice(unittest.TestCase):
	
	"""This class class test the method of priyajain_codingexercise.py"""

	def setUp(self):
		self.expected_output = {'Company-A' : {'max_price' : 1000, 'period' : '1990_Aug'},\
		 			'Company-B' : {'max_price' : 1000, 'period' : '1990_Dec'},\
					'Company-C' : {'max_price' : 999, 'period' : '1991_Apr'},
					'Company-D' : {'max_price' : 1000, 'period' : '1990_Sep'},\
					'Company-E' : {'max_price' : 987, 'period' : '1990_Nov'}}
		
		self.file = open('sample.csv')
		
		self.share_sample_file = CompanyStock('sample.csv')
		
		self.expected_mapping_dict = {'Company-A':2, 'Company-B':3, 'Company-C':4, 'Company-D':5, 'Company-E':6}


	def tearDown(self):
		self.file.close()

	def test_get_max_share_1(self):
		actual_output = self.share_sample_file.get_max_share1()
		for key in self.expected_output.keys():
			self.assertEqual(self.expected_output[key]['period'].upper(), actual_output[key]['period'].upper())
			self.assertEqual(str(self.expected_output[key]['max_price']), str(actual_output[key]['max_price']))

	def test_get_max_share_2(self):
		actual_output = self.share_sample_file.get_max_share2()
		for key in self.expected_output.keys():
			self.assertEqual(self.expected_output[key]['period'].upper(), actual_output[key]['period'].upper())
			self.assertEqual(str(self.expected_output[key]['max_price']), str(actual_output[key]['max_price']))
	
	def test_create_mapping_dict(self):
		actual_output = self.share_sample_file.create_mapping(self.file.readline())
		for key in self.expected_mapping_dict.keys():
			self.assertEqual(self.expected_mapping_dict[key], actual_output[key])


if __name__ == "__main__":
	suite = unittest.TestLoader().loadTestsFromTestCase(TestCompanySharePrice)
    	unittest.TextTestRunner(verbosity=2).run(suite)            
   	sys.exit()