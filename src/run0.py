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
	Location



###OUTPUTS:####
report.csv 
File must contain variables Border,Date,Measure,Value,Average
File must be unique at Border*Date*Measure
File must be sorted (desc) by date, value, measure, border




####PROGRAM SUMMARY######
### STEP 1 : READIN INPUT AND REFORMAT
### 1A REFORMAT VARIABLES TO BE THE TYPE I WILL NEED
### 1B REDUCE SIZE: keep only the fields I care about
### For the purposes of this challenge, 
###you'll want to pay attention to the following fields:
Border: Designates what border was crossed
Date: Timestamp indicating month and year osf crossing
Measure: Indicates means, or type, of crossing being measured (e.g., vehicle, equipment, passenger or pedestrian)
Value: Number of crossings


#### STEP 2 : CREATE SUMMARY STATISTICS FOR EACH BORDER*MEASURE*DATE
#### 2A. SORT DATA SO THAT I CAN USE INTERTOOLS.GROUPBY 
#### 2B. FOR EACH BORDER*MEASURE*DATE CALCULATE NUMBER OF CROSSINGS
#### 2C. WITHIN EACH BORDER*MEASURE, APPEND MOVING AVERAGE FOR THAT MONTH
#### 2D. TRANSFORM RUNNING TOTAL 
####FOR EACH BORDER*CROSSING TYPE (aka measure) , CALCULATE:
		FOR EACH MONTH:
			TOTAL CROSSINGS
			ROUND(PREVIOUS MONTH'S RUNNING TOTAL DIVIDED BY THIS MONTHS ORDER IN TIME)





SORT OUTPUT FILE
MAKE SURE IT CONTAINS THE RIGHT VARIABLES
MAKE SURE IT IS KEYED AT THE RIGHT LEVEL
MAKE SURE IT HAS THE RIGHT NUMBER OF ROWS (AKA UNIQUE CROSSTABS OF KEYS INCLUDING EMPTY MONTHS OR CATEGORIES)

"""



#!/usr/bin/python3
import csv
import os
import operator
import itertools
import datetime
import locale
import collections
import re
from dateutil.relativedelta import relativedelta



#Set global locale preference to US locale
locale.setlocale(locale.LC_TIME, "en_US") 
def PrintNRows(iterable_object, Nrows = 4):
	for i, row in enumerate(iterable_object):
		print(i,row)
		if (i >= (Nrows-1)):
			break


def CleanWhitespace(string_in):
	#convert all contiguous whitespace to be single space 
	#remove leading and trailing whitespace,
	cleaned_string = re.sub(r'\s+', ' ', string_in).strip()
	return cleaned_string

def StringToFloat(string_in):
	#impute missing values to zero
	#else convert to float
	if CleanWhitespace(string_in) == '':
		return 0.00
	else:
		return float(string_in)
	return string_as_float

def DateToString(datetime_in):
    		return datetime_in.strftime("%m/%d/%Y %I:%M:%S %p")

# Define  global variables
input_filepath = os.path.join(os.getcwd(), '../input/small_Border_Crossing_Entry_Data.csv')

#########
#STEP 1 : read in dataset, 
#make sure data conforms to desired formats
#keep track of unique values of border,measure
#keep track of min/max date 
#########
input0 = [] #input data 
unique_values_border, unique_values_measure, unique_values_date = set(), set(), set()
with open(input_filepath) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
    	# convert the Date variable which is a string to be a datetime, in 12-hour format
  		# allow for irregularity in whether we receive datetime or just date
    	yearmonth_as_datetime0 = datetime.datetime.strptime(row['Date'][:10], "%m/%d/%Y")
    	#collapse that date into a yearmonth, set at midnight of the first of the month
    	yearmonth_as_datetime1 = datetime.datetime(
    		year = yearmonth_as_datetime0.year,
    		month = yearmonth_as_datetime0.month,
    		day = 1, 
    		hour = 0,
    		minute = 0,
    		second = 0)
    	
    	#reformat for appending into input0
    	yearmonth_out = DateToString(yearmonth_as_datetime1)
    	border_out = CleanWhitespace(row['Border'])
    	measure_out = CleanWhitespace(row['Measure'])


    	#add to set if unique value
    	unique_values_border.add(border_out)
    	unique_values_date.add(yearmonth_as_datetime1)
        unique_values_measure.add(measure_out)
        
    	
    	#prepare output: keep only border, date, measure, and value
    	output_keys = ['Border','Date','Measure','Value']
    	output_values = [border_out,
    					yearmonth_out,
    					measure_out,
    					StringToFloat(row['Value'])
    					]

    	#add rows to input0
    	input0.append(dict(zip(output_keys,output_values))) 







#########
#STEP 2 : PAD MY DATASET WITH ZEROS WHERE NECESSARY
#########
#Before summarizing, data must contain one row per border*measure*month
#If a given combination doesnt exist in data, must pad with zeros.


date_range = []
lastmonth = max(unique_values_date)
firstmonth = min(unique_values_date)

while firstmonth <= lastmonth:
    date_range.append(DateToString(firstmonth))
    firstmonth += relativedelta(months=1)


cartesian_product_unique_values = itertools.product(unique_values_border,unique_values_measure,date_range)
list_unique_tuples = list(cartesian_product_unique_values)

list_of_dicts_unique_combos = []
for tup in list_unique_tuples:
	dict_out = {'Border':tup[0], 'Measure':tup[1], 'Date':tup[2]}
	list_of_dicts_unique_combos.append(dict_out)


#print(list(unique_values_border))
#print(list(itertools.combinations(list_of_unique_sets,r=2)))
print(list_of_dicts_unique_combos)



#########
#STEP 3 : CREATE A NESTED FOR-LOOP FOR SUMMARY STATISTICS
#########

sorted_input = sorted(input0, key=operator.itemgetter('Border', 'Measure', 'Date'))
print("******PRINT UNSORTED FIRST FEW ROWS******")
PrintNRows(input0, Nrows = 10)
print("******PRINT SORTED FIRST FEW ROWS******")
PrintNRows(sorted_input,10)




print("within each border*measure, figure out how many crossings there were per date and moving average")
host_data = []
for i,j in itertools.groupby(sorted_input, key=lambda x:(x['Border'], x['Measure'])):
	running_total_previous_month = 0
	index_this_month = 1
	for k,l in itertools.groupby(j, key=lambda x:(x['Date'])):
		if index_this_month == 1:
			moving_average = 0
		else:
			moving_average = int(round(running_total_previous_month/(index_this_month-1)))
		total_this_month = sum(row['Value'] for row in l)
		returndict = {'sum':total_this_month, 'moving_average':moving_average}

		print(type(i))
		returndict = {'Border':i[0], 'Measure':i[1], 'Date':k, 'sum':total_this_month,'moving_avg': moving_average}
		host_data.append(returndict)
		index_this_month = index_this_month + 1
		running_total_previous_month = running_total_previous_month + total_this_month

#PrintNRows(host_data,10)
