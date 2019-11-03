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