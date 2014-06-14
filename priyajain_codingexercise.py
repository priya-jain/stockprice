#Run this file from command prompt using the command 'python <filename1.py> <filename2.csv>'.

#Example D:\priya\Python27>python D:\\priya\\project\\comapnystock\\priyajain_codingexercise.py D:\\priya\\project\\comapnystock\\sample.csv

#This module contains two implementation for the problem 'getmaxshare1' and 'getmaxshare2'.

#The output of the problem will be in two file report1.csv and report2.csv which will be created when we run this script.

#The location of the output files will be present working directory.

import csv
import sys

class invalidFile(Exception):
	pass

class CompanyStock():
	def __init__(self, input_file=None):
		if not input_file:
			pass
		self.file_name = input_file
		try:
			self.file = open(input_file)
			self.header = self.file.readline()
			self.list = self.getListOfRows()
			self.mapping_dict = self.create_mapping(header = self.header)
		except Exception as e:
			print "Unable to open file. Reason {0}".format(e)

	'''This method creates a dictionary which contains the data of each company 
	for each month of each year. This dictionary can be used for reporting purpose.'''
	def FormatData(self):
		_dict = {key : {} for key in self.mapping_dict.keys()} 
		temp = {}
		for item in self.list:
			item_arr = item.strip().split(",")
			year_month = str(item_arr[0])+'_'+item_arr[1]
			for key, value in self.mapping_dict.iteritems():
				_dict[key][year_month] = item_arr[value] 		
		return _dict
			

	#This method find the maximum price of shares for each company and stores the result in a dict.
	def getMaxShare1(self): 
		max_share = {key : 0 for key in self.mapping_dict.keys()}
		max_share_year = {key : '' for key in self.mapping_dict.keys()}
		for item in self.list:
			item_arr = item.strip().split(",")
			year_month = str(item_arr[0])+'_'+item_arr[1]
			for key, value in self.mapping_dict.iteritems():
				if int(item_arr[value]) > int(max_share[key]):
					temp = {'period':year_month, 'max_price': item_arr[value]}
					max_share_year[key] = temp  
					max_share[key] = item_arr[value] 
			
		return max_share_year
	
	#This method find the maximum price of shares for each company and stores the result in a dict. This method uses the csv module.
	def getMaxShare2(self):
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
				
		

	'''This method creates a new file and write the maximum price of the company in that file.
	This method calls the getMaxShare1() of this class.'''
	
	def getReport1(self, file_name):
		try:
			max_price_year_dict = self.getMaxShare1()
			_file = open(file_name, 'w')
			for key in max_price_year_dict .keys():		
				_file.write("%s got maximum share price $ %s in %s\n" %(key, max_price_year_dict[key]['max_price'], max_price_year_dict[key]['period']))
			_file.close()
		except Exception as msg:
			print "Error Occurred while opening the file <{0}>. Reason {1}".format(file_name, msg)

	'''This method creates a new file and write the maximum price of the company in that file. 
	This method calls the getMaxShare2() of this class.'''
	
	def getReport2(self, file_name):
		max_price_year_dict = self.getMaxShare2()
		try:
			_file = open(file_name, 'w')
			for key in max_price_year_dict .keys():		
				_file.write("%s got maximum share price $ %s in %s\n" %(key, max_price_year_dict[key]['max_price'], max_price_year_dict[key]['period']))
			_file.close()
		except Exception as msg:
			print "Error Occurred while opening the file <{0}>. Reason {1}".format(file_name, msg)


	#This method returns the list of strings which are row in the file separated by \n

	def getListOfRows(self):
		return [line for line in self.file]

	#This method returns a dictionary which maps the company name with the corresponding index of the header.	
	
	def create_mapping(self, header=None):
		if not header:
			raise invalidFile
		
		header_arr = header.strip().split(',')

		#Loop over the header of the file and create a dict object which maps company name with their index.
		_dict = {str:index for index, str in enumerate(header_arr)}
		_dict.pop('Year')
		_dict.pop('Month')
		return _dict
		
		

if __name__ == "__main__":
	try :
		share = CompanyStock(sys.argv[1])
		share.getReport1("report1.csv") #First implementation : No in-built module is used to produce the desired result.
		share.getReport2("report2.csv") #second implementation : module named 'CSV' is used to produce the desired result.
	except Exception as e:
		print "Error Occurred in main. Reason {0}".format(e)				
		
		
		