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
	Port Name
	State
	Port Code
	Border
	Date
	Measure
	Value
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


# Set some global preferences and define custom function(s)
locale.setlocale(locale.LC_TIME, "en_US") # make sure that datetime output will be in US locale (AM/PM)
def PrintNRows(iterable_object, Nrows = 4):
	for i, row in enumerate(iterable_object):
		print(i,row)
		if (i >= (Nrows-1)):
			break

# Define some global variables literals
input_filepath = os.path.join(os.getcwd(), '../input/small_Border_Crossing_Entry_Data.csv')
keep_only_these_vars = ['Border','Date','Measure','Value']

#########
#STEP 1 : read in dataset, collapse timestamps to yearmonth values, keep only necessary columns using keep_only_these_vars
#########
indat0 = [] #input data version 0
with open(input_filepath) as csvfile:
    reader = csv.DictReader(csvfile
    	#, fieldnames=('Port Name','State','Port Code','Border','Date','Measure','Value','Location')
    	)
    for row in reader:
    	row['Value'] = float(row['Value'])*1.00
    	# convert the Date variable which is a string to be a datetime, in 12-hour format
    	yearmonthdaysecond_as_datetime = datetime.datetime.strptime(row['Date'], "%m/%d/%Y %I:%M:%S %p")
    	#collapse that datetime into a yearmonth, set at midnight of the first of the month
    	yearmonth_as_datetime = datetime.datetime(
    		year = yearmonthdaysecond_as_datetime.year,
    		month = yearmonthdaysecond_as_datetime.month,
    		day = 1, 
    		hour = 0,
    		minute = 0,
    		second = 0)
    	yearmonth_as_string = yearmonth_as_datetime.strftime("%m/%d/%Y %I:%M:%S %p")
    	row['Date'] = yearmonth_as_string
    	#when I convert yearmonth_as_datetime back to string, it must MATCH original Date string else break
    	"""
    	if row['Date'] != yearmonth_as_datetime.strftime("%m/%d/%Y %I:%M:%S %p"):
    			print("SOMETHING IS UP W YOUR DATETIMES BRO: these must match and they dont")
    			print("this is original row[date]")
    			print(row['Date'])
    			print("this is original converted to datestamp collapsed to yearmonth")
    			break
    	print(row['Date'])
    	print(yearmonthdaysecond_as_datetime)
    	print(yearmonthdaysecond_as_datetime.strftime("%m/%d/%Y %I:%M:%S %p"))
    	print(yearmonth_as_datetime)
    	print(yearmonth_as_string)
    	print('***')
    	"""
    	indat0.append({ keptvar: row[keptvar] for keptvar in (keep_only_these_vars +[]) }) 



#########
#STEP 2 : PAD MY DATASET WITH ZEROS TO ENSURE NUMBER OF ROWS
#########



#########
#STEP 3 : CREATE A NESTED FOR-LOOP FOR SUMMARY STATISTICS
#########

indat1 = sorted(indat0, key=operator.itemgetter('Border', 'Measure', 'Date'))
print("******PRINT UNSORTED FIRST FEW ROWS******")
PrintNRows(indat0, Nrows = 10)
print("******PRINT SORTED FIRST FEW ROWS******")
PrintNRows(indat1,10)

print("for each border*measure*date, figure out how many crossings there were")
host_data = []
for k,v in itertools.groupby(indat1, key=lambda x:({'Border':x['Border'], 'Measure':x['Measure'], 'Date': x['Date']})):
	returndict = {'sum':sum(row['Value'] for row in v)}
	returnsNone =  returndict.update(k)
	host_data.append(returndict)

PrintNRows(host_data,10)




print("for each border*measure, figure out how many crossings there were")
host_data = []
for i,j in itertools.groupby(indat1, key=lambda x:(x['Border'], x['Measure'])):
	running_total_previous_month = 0
	index_this_month = 1
	for k,l in itertools.groupby(j, key=lambda x:(x['Date'])):
		if index_this_month == 1:
			moving_average = 0
		else:
			moving_average = int(round(running_total_previous_month/(index_this_month-1)))
		total_this_month = sum(row['Value'] for row in l)
		newrow = {'grouping':(i,k), 'sum':total_this_month,'moving_avg': moving_average}
		host_data.append(newrow)
		index_this_month = index_this_month + 1
		running_total_previous_month = running_total_previous_month + total_this_month

PrintNRows(host_data,10)

print(type(host_data[1]['grouping']))