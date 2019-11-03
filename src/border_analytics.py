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
from define_functions import *


	

# Define  global variables
thisfile_path = Path(__file__)
project_directory = thisfile_path.parent.parent
input_filepath = project_directory / 'input' / "large_Border_Crossing_Entry_Data.csv"
output_filepath = project_directory / 'output' / "report.csv"
datetime_format_options_filepath = project_directory / 'src' / "acceptable_date_formats.py"




exec(open(datetime_format_options_filepath).read())



#########
# STEP 1 : read in dataset,
# make sure data conforms to desired formats
# keep track of unique values of border,measure
# keep track of min/max date
#########
input0 = []  # object that will be my input data
with open(input_filepath, newline = '', mode ='r') as csvfile:
    try:
        csv.Sniffer().sniff(csvfile.read(1024))  # take a 1024B (max) portion of the file and try to get the Dialect
        csvfile.seek(0)
    except csv.Error:
        print('Error Reading CSV')

unique_values_date = set()  # keep track of unique dates
with open(input_filepath, newline = '',mode = 'r') as csvfile:
	reader = csv.DictReader(csvfile)
	for row in reader:
		# convert the Date variable which is a string to be a datetime
		# Keep only 1st 10 characters to allow for irregularity in date/datetime input
		yearmonth_as_datetime0 = StringToDate_ManyFormats(str_in = row['Date'])
		# collapse that date into a yearmonth, set at midnight of the first of the month
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
		value_out = int(row['Value'])

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



#########
#STEP 2 : PAD input DATASET WITH ZEROS WHERE NECESSARY
#########
#Before summarizing, I must pad data with zeros for dates that do not appear
# for a given border*measure, if date doesnt exist, impute values with zero


#determine the range of dates that must exist for each border*measure
firstmonth=min(unique_values_date)
lastmonth=max(unique_values_date)


#I want to groupby . this necessitates sorting
sorted_input = sorted(input0, key=operator.itemgetter('Border', 'Measure'))

summarised_data = []
for i,j in itertools.groupby(sorted_input, key=lambda x:(x['Border'], x['Measure'])):
	#i is a tuple that defines the key of the groupby
	#j is a grouped object that, when converted to list, is a list of dicts 
	## this list of dicts is all the available data rows for that border*measure 
	## that is the sub-object we are iterating by
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



