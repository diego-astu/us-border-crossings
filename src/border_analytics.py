"""
TEST IDEAS:
* Change around formats in excel:
* * * 
* Add weird characters in excel:
* * * comma in the middle of a string
* * * comma in the end of a string
* * * comma in the beginning of a string
* * * first char of a cell is a comma
* * * last char of a cell is a comma
* * * first char of first cell is a comma
* * * last char of last cell is a comma
* * * all of the above but for newline characters n and r
* Value Field Formatting
* * * Value field is manually formatted numeric
* * * Value field has comma or point separators
* * * Value field has decimal points
* * * Value field has non-numeric characters
* * * Scientific Notation
* Date Field Formatting
* * * Try a wide variety of date formats
* Text Field possible formatting troubles
* * * What if dates are in different formats
* * * What if theres a comma in one of the fields
* * * What if theres 2 commas in one of the fields
* * * What if two fields have a comma
* * * What if the columns in the csv are in different orders
* Data cardinality edge cases
* * * What if there are no rows
* * * What if only one row (one border*measure*date)
* * * What if only one border*measure*date Category (but many rows)
* * * What if only one Border*measure Category
* * * What if only one Border*date Category
* * * What if only one Measure*date Category
* * * What if only one Morder Category
* * * What if only one Date Category
* * * What if only one Measure Category
* Data missigness
* * * What if a  field is blank?
* * * What if a  field is =na()?
* * * What if a  field is a single quote
* * * What if a  field is a double quote
* * * What if a  field is 2 single quotes
* * * What if a  field is 2 double quotes
* * * What if a  field is 3 single quotes
* * * What if a  field is 3 double quotes
* * * What if a  field is 4 single quotes
* * * What if a  field is 4 double quotes
* * * WHat if an entire row is missing
"""


"""
##############OVERVIEW##############
For this challenge, we want to you to 
calculate the total number of times 
vehicles, equipment, passengers and pedestrians 
cross the 
U.S.-Canadian and U.S.-Mexican borders 
each month. 

We also want to know the 
running monthly average of total number of crossings 
for that type of 
crossing and border.


###INPUTS:####
Border_Crossing_Entry_Data.csv 
ALl columns will be read as strings, but can be converted
COLUMNS : 
	Port Name (ignore)
	State (ignore)
	Port Code (ignore)
	Border (keep)
	Date (keep)
	Measure (keep)
	Value (keep)
	Location (ignore)



###OUTPUTS:####
report.csv 
File must contain variables Border,Date,Measure,Value,Average
File must be unique at Border*Date*Measure
File must be sorted (desc) by date, value, measure, border




####SCRIPT SUMMARY######
### STEP 1 : READIN INPUT AND ENSURE PROPER FORMAT
### 1A REFORMAT VARIABLES: DictReader can only read strings
### 1B REDUCE SIZE: keep only the fields I care about


#### STEP 2 : PREPARE DATA FOR SUMMARIZING
#### If a given border*meausure combination does not exist, no problem
#### But if for a given border*measure, there are missing date entries
#### That will make my moving average incorrect (need to pad with zeros)
#### Within each border*measure combination, insert value 0 for missing dates


#### STEP 3 : CREATE SUMMARY STATISTICS FOR EACH BORDER*MEASURE*DATE
#### 3A. SORT DATA SO THAT I CAN USE INTERTOOLS.GROUPBY 
#### 3B. FOR EACH BORDER*MEASURE*DATE CALCULATE NUMBER OF CROSSINGS
#### 3C. WITHIN EACH BORDER*MEASURE, APPEND MOVING AVERAGE FOR THAT MONTH
#### 3D. TRANSFORM RUNNING TOTAL 
####FOR EACH BORDER*CROSSING TYPE (aka measure) , CALCULATE:
		FOR EACH MONTH:
			TOTAL CROSSINGS
			ROUND(PREVIOUS MONTH'S RUNNING TOTAL DIVIDED BY THIS MONTHS ORDER IN TIME)





SORT OUTPUT FILE
FILTER TO ONLY INCLUDE CASES WITH VALUE = 0
MAKE SURE IT CONTAINS THE RIGHT VARIABLES
MAKE SURE IT IS KEYED AT THE RIGHT LEVEL
MAKE SURE IT HAS THE RIGHT NUMBER OF ROWS (AKA UNIQUE CROSSTABS OF KEYS INCLUDING EMPTY MONTHS OR CATEGORIES)

"""



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





def my_round(num_in, round_to = 0):
	twice_my_num = num_in * 2
	# if twice my number is a whole number then 
	# using the normal round function will use
	# bankers rounding and i want integer rounding
	if twice_my_num % 1 == 0 :
		return ceil(num_in)
	else:
		return round(num_in,round_to)


def CleanWhitespace(string_in):
	#convert all contiguous whitespace to be single space
	#remove leading and trailing whitespace,
	cleaned_string = re.sub(r'\s+', ' ', string_in).strip()
	return cleaned_string





def IncreaseMonthByOne(datetime_in):

	#Inputs: 
	## datetime_in must be a datetime object set at year/month at midnight of first day
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





def PadDictlistWithCustomValues(key, value, my_dictlist, key_to_impute, imputed_value = 0.00):
	#This function scans a dictlist (my_dictlist) for a key:value pair
	#If key:value pair is found, it returns dictlist as-is
	#If not, it returns an augmented dictlist with ONE additional row
	#The additional row is a copy of the FIRST row, with TWO modifications
	### modify the key:value pair, and impute one additional value in dict
    for dict_i in my_dictlist:
        if any(dict_i[key] == value for dict_i in my_dictlist):
            return my_dictlist
        else:
        	#create new temp dict . shallow copy OK bc not compound object
        	dict_j = dict(dict_i)
        	#modify the temp dict so it has the missing key:value pair.
        	dict_j[key] = value
        	#perform imputation
        	dict_j[key_to_impute] = imputed_value
        	ReturnsNone = my_dictlist.extend([dict(dict_j)])
        	return my_dictlist

# Define  global variables
thisfile_path = Path(__file__)
project_directory = thisfile_path.parent.parent
input_filepath = project_directory / 'input' / "Border_Crossing_Entry_Data.csv"
output_filepath = project_directory / 'output' / "report.csv"




#########
# STEP 1 : read in dataset,
# make sure data conforms to desired formats
# keep track of unique values of border,measure
# keep track of min/max date
#########
input0 = []  # object that will be my input data


#year and month is obligatory
#In excel, the only formats where day appears before month is when month is written


def StringToDate_ManyFormats(str_in):
	# allow for equivalency of dash and / remove comma
	str_in1 = str_in.replace('-','/').replace(',','')

	
		try:
			return datetime.datetime.strptime(str_in, date_format)
		except ValueError:
			pass
	raise ValueError('Cant parse that date format:', str_in)
	


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
					'Date':datetime_in.strftime("%m/%d/%Y %I:%M:%S %p"), 
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

