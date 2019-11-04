#!/usr/bin/python3
import csv
from pathlib import Path
import os
import operator
import itertools
import datetime
import locale
import collections
import re
import datetime
from fractions import Fraction
from math import ceil
import copy
import time
import string

	
def my_round(num_in):
	# INPUTS: NON-NEGATIVE FLOAT
	# OUTPUT: NON-NEGATIVE INTEGER

	num_in = float(num_in)

	if num_in < 0.00:
		raise ValueError("Input to my_round() must be a non-negative number")
	

	twice_my_num = num_in * 2
	
	# if twice my number is a whole number then 
	# using the normal round function will use
	# bankers rounding and i want integer rounding
	if twice_my_num % 1 == 0 :
		return ceil(num_in)
	else:
		return round(num_in)


def CleanWhitespace(string_in):
	if not isinstance(string_in,str):
		raise ValueError("Input to CleanWhitespace() must be a string")

	#convert all contiguous whitespace to be single space
	#remove leading and trailing whitespace,
	cleaned_string = re.sub(r'\s+', ' ', string_in).strip()
	return cleaned_string


def IncreaseMonthByOne(datetime_in):
	#Inputs: 
	## datetime_in must be a datetime object set at year/month at midnight of first day
	if not isinstance(datetime_in,datetime.datetime):
		raise TypeError("Input to IncreaseMonthByOne() must be a datetime")
	if not datetime_in.day == 1:
		print(datetime_in, 'day is:',datetime_in.day)
		raise ValueError("hour, minute, and second of datestamp feeding IncreaseMonthByOne() must be set to zero")

	if not (datetime_in.hour == 0 and datetime_in.minute == 0 and datetime_in.second == 0):
		print(datetime_in, 'hour/min/sec are:', (datetime_in.hour, datetime_in.minute, datetime_in.second))
		raise ValueError("hour, minute, and second of datestamp feeding IncreaseMonthByOne() must be set to zero")
	
	#Output:
	## Must return a datetime object with same features as input, one month ahead
	
	if datetime_in.month < 12:
		return datetime.datetime(
			year=datetime_in.year,
			month=(datetime_in.month + 1),
			day=datetime_in.day,
			hour=datetime_in.hour,
			minute=datetime_in.minute,
			second=datetime_in.second)
	else:
		return datetime.datetime(
			year=datetime_in.year + 1,
			month=1,
			day=datetime_in.day,
			hour=datetime_in.hour,
			minute=datetime_in.minute,
			second=datetime_in.second)


def RemoveNonNumeric(str_in):
	if not isinstance(str_in,str):
		raise TypeError("Input to RemoveNonNumeric() must be a string")
	str_out = re.sub("[^0-9]", "", str_in)
	return str_out



def PadDictlistWithCustomValues(key, value, my_dictlist, key_to_impute, imputed_value = 0.00):
	if not isinstance(my_dictlist,list):
		raise TypeError("Input to PadDictlistWithCustomValues() must be a list")
	for i in list(range(0,len(my_dictlist)-1)):
		if not isinstance(my_dictlist[i],dict):
			raise TypeError("index",i, "in my_dictlist input to PadDictlistWithCustomValues() is not a dict")
		if not key in list(my_dictlist[i].keys()):
			#list(my_dictlist[i].keys):
			print(my_dictlist[i])
			raise ValueError("key argument,",key,"must exist in every dict inside my_dictlist")

	#This function scans a dictlist (my_dictlist) for a key:value pair
	#******The argument for key must exist in every dict inside my_dictlist******
	#If key:value pair is found, it returns dictlist as-is
	#If not, it returns an augmented dictlist with ONE additional row
	#The additional row is a copy of the FIRST row, with TWO modifications
	### modify the key:value pair to match arguments, and impute one additional value in dict
	for dict_i in my_dictlist:
		if any(dict_i[key] == value for dict_i in my_dictlist):
			return my_dictlist
			
		else:
			dict_j = dict(dict_i) #create new temp dict . shallow copy OK bc not compound object
			dict_j[key] = value #modify the temp dict so it has the missing key:value pair.
			dict_j[key_to_impute] = imputed_value #perform imputation
			ReturnsNone = my_dictlist.extend([dict(dict_j)])
			return my_dictlist



def CombineComponents(dict_in):
	keys = dict_in.keys()
	#This function reads in a dictionary, 
	#extracts the keys and the values, and 
	#returns combinations of keys & values as a DictList

	values = (dict_in[key] for key in keys)
	combinations = [dict(zip(keys, combination)) for combination in (itertools.product(*values))]
	return combinations

def RemoveKeysListofDicts(LOD_in,keygone):
	#This function reads in a list of dicts and subsets it
	#It removes key:value pairs specified by keys in keygone
	listofdicts = copy.deepcopy(LOD_in)
	for d in listofdicts:
		del d[keygone]
	return listofdicts
def DictlistToStringlist(dictlist_in):
	#this function reads in a list of dicts 
	#iterates through each value and appends it to a list
	#outputs a list of strings
	outlist = []
	for d in dictlist_in:
		stringyy = ''
		for v in d.values():
			stringyy = stringyy+ str(v)
		outlist.append(stringyy)
	return outlist



def StringToDate_ManyFormats(str_in,list_of_formats = ["%m/%d/%Y %H:%M:%S %p"] ):
	if str_in is '':
	 return ''
	# I am able to cover every format that appears in excel using this function
	# except Wednesday, March 14, 2012
	# strptime accepts the above with one of two commas
	str_in1 = str_in.replace(',','').replace('-','/')
	# Solution : replace comma with blank
	# Also allow dashes to be used instead of slashes
	for date_format in list_of_formats:
		try:
			return datetime.datetime.strptime(str_in1, date_format)
		except ValueError:
			try:
				return datetime.datetime.strptime(time.ctime(float(str_in)),"%m/%d/%Y %H:%M:%S %p")
			except ValueError:
				pass
	raise ValueError('Cant parse', str_in, '->', str_in1,'as',date_format)






def ReadValue_ManyFormats(str_in):
	## This function reads in a string which must be convertible to an integer
	str_wk = CleanWhitespace(str_in)
	if str_wk == '':
		return 0
	if 'e' in str_wk.lower():
		#this is scientific notation
		return int(float(str_wk))
	elif '%' in str_wk.lower():
		#this is a percentage
		remove_percent_symbol = str_wk.split("%")[0]
		
		return int(float(remove_percent_symbol)/float(100.0))
	else:
		remove_decimals = str_wk.split(".")[0]
		remove_nonumeric = RemoveNonNumeric(remove_decimals)
		if remove_nonumeric == '':
			return 0
		else:
			return int(remove_nonumeric)

