"""
This module can be used to find the maximum share price the company. This script accepts a CSV file as the second argument at
command line and produce the desired result. 

To run this script use the following command at the command prompt : python <filename1.py> <filename2.csv>

<filename1.py> -> is the path of the script file 
<filename2.csv> -> is the path of the csv file which contains the company stock data.

This module contain two implementation methods for the problem as 'get_max_share1' & 'get_max_share2'.

The output of the problem will be in two file report1.csv and report2.csv which will be created when we run this script.

The location of the output files will be present working directory.

"""

import csv
import sys

class InvalidFile(Exception):
	pass

class CompanyStock():

	"""This class creates CompanyStock object which we can use to get maximum-price of each company"""
	
	def __init__(self, input_file=None):
		"""The constructor initialises the instance variable.
		
		self.file -> It is the CSV file which contains the data of share prices for the companies.
		self.header -> It is list of columns of the header(first row) in the CSV file.
		self.list -> It is the list of rows of the CSV file.
		self.mapping_dict -> It is a dictionary which contains company name as keys and their corresponding index as values.
		"""
		if not input_file:
			pass
		self.file_name = input_file
		try:
			self.file = open(input_file)
			self.header = self.file.readline()
			self.list = self.get_list_of_rows()
			self.mapping_dict = self.create_mapping(header = self.header)
		except Exception as e:
			print "Unable to open file. Reason {0}".format(e)

	def format_data(self):
		"""This method creates a dictionary which contains the data of each company.
		
		The dictionary would contain data for each month of each year.
		This dictionary can be used for reporting purpose.
		"""
		_dict = {key : {} for key in self.mapping_dict.keys()} 
		temp = {}
		for item in self.list:
			item_arr = item.strip().split(",")
			year_month = str(item_arr[0])+'_'+item_arr[1]
			for key, value in self.mapping_dict.iteritems():
				_dict[key][year_month] = item_arr[value] 		
		return _dict
			
	def get_max_share1(self):
		"""This method find the maximum price of shares for each company.

		This method stores the result in a dict.
		"""
		max_share = {key : 0 for key in self.mapping_dict.keys()}  
		max_share_year = {key : '' for key in self.mapping_dict.keys()}
		for item in self.list:  #self.list contains the list of strings and each string is separated by ','
			item_arr = item.strip().split(",")  
			year_month = str(item_arr[0])+'_'+item_arr[1]
			
			#here key will be the company name and value will be the index of the company present in the csv.
			for key, value in self.mapping_dict.iteritems(): 
				if int(item_arr[value]) > int(max_share[key]):
					temp = {'period':year_month, 'max_price': item_arr[value]}
					max_share_year[key] = temp  
					max_share[key] = item_arr[value] 
			
		return max_share_year
	
	def get_max_share2(self):
		"""This method find the maximum price of shares for each company.

		This method stores the result in a dictionary. This method uses the csv module.
		"""
		try:
			with open(self.file_name) as f:
				_file = csv.DictReader(f)
				field_names =  set(_file.fieldnames)
				company_name = field_names - {'Year', 'Month'}
				max_price = 0
				max_price_dict = {}
				for row in _file:
					for company, price in row.items():
						if company not in company_name:
							continue
						if max_price_dict.has_key(company):
							 if int(price) > int(max_price_dict[company]['max_price']):
								max_price_dict[company]['max_price'] = price
								max_price_dict[company]['period'] = str(row['Year']+'_'+row['Month'])
						else:
							max_price_dict[company] = {'period':'', 'max_price' : 0}
		except (Exception) as e:
        		print "Error occurred : Reason - {0}",format(e)
		return max_price_dict			
	
	def get_report1(self, file_name):
		"""This method creates a new file.

		This method write the maximum price of the company in that file.		
		This method calls the get_max_share1() of this class.
		"""
		try:
			max_price_year_dict = self.get_max_share1()
			_file = open(file_name, 'w')
			for key in max_price_year_dict .keys():		
				_file.write("%s got maximum share price $ %s in %s\n" 
							%(key, max_price_year_dict[key]['max_price'],
							max_price_year_dict[key]['period']))
			_file.close()
		except Exception as msg:
			print "Error Occurred while opening the file <{0}>. Reason {1}".format(file_name, msg)

	
	def get_report2(self, file_name):
		"""This method creates a new file.

		This method write the maximum price of the company in that file. 
		This method calls the get_max_share2() of this class
		"""
		max_price_year_dict = self.get_max_share2()
		try:
			_file = open(file_name, 'w')
			for key in max_price_year_dict .keys():		
				_file.write("%s got maximum share price $ %s in %s\n" 
							%(key, max_price_year_dict[key]['max_price'],
							max_price_year_dict[key]['period']))
			_file.close()
		except Exception as msg:
			print "Error Occurred while opening the file <{0}>. Reason {1}".format(file_name, msg)


	
	def get_list_of_rows(self):
		"""This method returns the list of strings which are row in the file separated by \n."""
		return [line for line in self.file]

		
	def create_mapping(self, header=None):
		"""This method returns a dictionary which maps the company name with the corresponding index of the header."""
		if not header:
			raise InvalidFile
		
		header_arr = header.strip().split(',')
		#Loop over the header of the file and create a dict object which maps company name with their index.
		_dict = {str:index for index, str in enumerate(header_arr)}
		_dict.pop('Year')
		_dict.pop('Month')
		return _dict
		
if __name__ == "__main__":
	try :
		share = CompanyStock(sys.argv[1])
		#First implementation : No in-built module is used to produce the desired result.
		share.get_report1("report1.csv") 
		#second implementation : module named 'CSV' is used to produce the desired result.
		share.get_report2("report2.csv")
	except Exception as e:
		print "Error Occurred in main. Reason {0}".format(e)