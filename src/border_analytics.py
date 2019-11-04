#!/usr/bin/python3
###########################
# Default Library Dependencies
###########################
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

###########################
# Define  global variables
###########################
#this file and project directory
thisfile_path = Path(__file__)
project_directory = thisfile_path.parent.parent
#input and output files
input_filepath = project_directory / 'input' / "Border_Crossing_Entry_Data.csv"
output_filepath = project_directory / 'output' / "report.csv"
#path to a helper script i will source directly in this script (not a function definition)
datetime_format_options_filepath = project_directory / 'src' / "acceptable_date_formats.py"


###########################
# Other Dependencies
###########################
# my custom helper functions
from define_functions import *
# execute a script that creates a list called final_list_of_datetime_strings
# This is a list of datetime formats my script will accept
exec(open(datetime_format_options_filepath).read())





#########
# STEP 1 : 
# read in dataset into list of dicts called input0
# make sure data conforms to desired formats (int,string,datetime)
# keep track of unique date values
#########
input0 = []  # object that will be my input data
unique_values_date = set()  # keep track of unique dates

with open(input_filepath, newline = '',mode = 'r') as csvfile:
	reader = csv.DictReader(csvfile,restval='')

	for row in reader:
		if (row['Date'] != '' and row['Border'] != '' and row['Measure'] != ''):
			# convert the Date variable which is a string to be a datetime
			# Keep only 1st 10 characters to allow for irregularity in date/datetime input
			
			yearmonth_as_datetime0 = StringToDate_ManyFormats(str_in = row['Date'],
				list_of_formats = final_list_of_datetime_strings)
			# collapse that date into a yearmonth, set at midnight of the first of the month

			if yearmonth_as_datetime0 == '':
				yearmonth_as_datetime1 = yearmonth_as_datetime0
			else:
				yearmonth_as_datetime1 = datetime.datetime(
					year=yearmonth_as_datetime0.year,
					month=yearmonth_as_datetime0.month,
					day=1,
					hour=0,
					minute=0,
					second=0)

			# reformat for appending into input0
			border_out = CleanWhitespace(row['Border'])
			measure_out = CleanWhitespace(row['Measure'])
			value_out = ReadValue_ManyFormats(row['Value'])

			# add to set if unique value
			unique_values_date.add(yearmonth_as_datetime1)

			# prepare output: keep only border, date, measure, and value
			output_keys = ['Border', 'Date', 'Measure', 'Value']
			output_values = [border_out,
							 yearmonth_as_datetime1,
							 measure_out,
							 value_out
							 ]

			# add rows (dicts) to input0 (list of dicts)
			input0.append(dict(zip(output_keys, output_values)))


print(input0)

#########
#STEP 2 : PAD DATA WITH ZEROS WHERE NECESSARY AND SUMMARIZE
#########
#Before summarizing, I must pad data with zeros for dates that do not appear
#determine the range of dates that must exist for each border*measure
firstmonth=min(unique_values_date)
lastmonth=max(unique_values_date)
summarised_data = []

#I want to groupby . this necessitates sorting
sorted_input = sorted(input0, key=operator.itemgetter('Border', 'Measure'))
for i,j in itertools.groupby(sorted_input, key=lambda x:(x['Border'], x['Measure'])):
	#i is a tuple that defines the key of the groupby
	#j is a grouped object that, when converted to list, is a list of dicts 
	## this list of dicts is all the available data rows for that border*measure 
	j_as_list = list(j)

	running_total_previous_month = 0
	index_this_month = 1
	this_month_datetime = firstmonth

	while this_month_datetime <= lastmonth:
		dictlist_augmented = PadDictlistWithCustomValues(
			key='Date', 
			value = this_month_datetime, 
			my_dictlist = j_as_list, 
			key_to_impute = 'Value', 
			imputed_value = 0)
		if index_this_month == 1:
			moving_average = 0.00
		else:
			moving_average = float(running_total_previous_month)/float(index_this_month-1)
		


		total_this_month = sum(int(row['Value']) for row in dictlist_augmented if row['Date'] == this_month_datetime)

		returndict = {'Border':dictlist_augmented[0]['Border'], 
					'Measure':dictlist_augmented[0]['Measure'], 
					'Date':this_month_datetime.strftime("%m/%d/%Y %I:%M:%S %p"), 
					'Value':total_this_month,
					'Average': int(my_round(moving_average))
					}

		summarised_data.append(returndict)
		summarised_data = list(filter(lambda d: d['Value'] > 0.0001, summarised_data))
	
		


		index_this_month = index_this_month + 1
		running_total_previous_month = running_total_previous_month + total_this_month
		this_month_datetime =  IncreaseMonthByOne(this_month_datetime)






out_data = sorted(summarised_data, key=operator.itemgetter('Date','Value','Measure','Average'), reverse=True)




with open(output_filepath, mode='w',newline ='') as output_file:
    dict_writer = csv.DictWriter(output_file, 
    	fieldnames = ['Border','Date','Measure','Value','Average'])
    dict_writer.writeheader()
    dict_writer.writerows(out_data)