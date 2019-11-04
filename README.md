# Border Crossing Analysis Exercise
JD Astudillo
Insight Data Engineering, Janary 2020 Cycle
Exercise completed : October 28 -November 3, 2019

# Key Files:
## run. sh: 
* Executes src/01_border-analytics.py, the main script
## src/01_border-analytics.py
* Import libraries & defines pathnames
* Import helper function definitions (from define_functions import *)
* Execute acceptable_date_formats.py, which yields list of acceptable Date formats
* Performs analytic exercise
    1) read in dataset into DictList called input0
    
        a) Format key data fields
        
        b) Keep track of unique date fields. Will iterate over them later.
    2) Summarize data into DictList called summarised_data
    
        a) Pad data with zero if dates do not appear. That is important for moving monthly average
        
    3) Sort data and output into /output/report.csv
## src/acceptable_date_formats.py
* This script produces a list called final_list_of_datetime_strings which contains all datetime formats my program will accept. 
* These formats come from all date formats seen in Excel (en_US locale) that specified a month and a year
* Structure:
    * There are only a handful of ways to express hour:minute:second. I list these out as DictLists manually
    * Year:month:day is more tricky.
        * There are several "formats" to express year/month/day
        * There are several valid permutations of those formats, which I call "Components" e.g. day-month-year, year-month-day. I express these Components as Dictionaries of Lists
        * Find all combinations of components that could make up a year:Month:day
        * Its possible to express monthyear without day, so some of these combinations should be subsetted and treated as separate combinations
    * After the above, I have lists of all the ways to express dates and times
        *  dictlist_all_time_combinations
        *  dictlist_all_date_combinations
    * There are some additional modifications to make, such as making it optional to specify time by adding a blank element to dictlist_all_time_combinations
    * Finally, we arrive at final_all_dates and final_all_times: These are all the accepted ways to format dates and times. The Combinations of these will be my final_list_of_datetime_strings
    * I have one duplicate in this list, because I force the default format ("%m/%d/%Y %H:%M:%S %p") to be at index 0.

## src/define_functions.py
* my_round(num_in, round_to = 0):
   * Turns out Python does banker's rounding as opposed to rounding to the nearest integer. That was a fun thing to learn...
   * This simple function performs rounding to the nearest integer
   * If twice num_in is a whole number, return ceil(num_in); else round()
* CleanWhitespace(string_in):
    * Convert all contiguous whitespace to be one space.
    * Trim trailing and leading whitespace
* IncreaseMonthByOne(datetime_in):
    * Takes in a datetime object with year/month specified and others truncated to zero
    * If December, returns January of year+1; else returns month+1
* RemoveNonNumeric(str_in):
    * substitutes all non-numeric characters with '' (empty string)
* PadDictlistWithCustomValues(key, value, my_dictlist, key_to_impute, imputed_value = 0.00):
    *  I use this function to "pad" my data with zeros (step 2a above)
    * Scans a dictlist (my_dictlist) for a key:value pair
    * If key:value pair is found, it returns dictlist as-is
    * Else, returns an augmented dictlist with ONE additional row:
        * The additional row is a copy of the FIRST row
        * The additional row has modified key and values, from first two arguments
* CombineComponents(dict_in):
    * This function reads in a dictionary
    * extracts the keys and the values
    * returns combinations of keys & values as a DictList  
* RemoveKeysListofDicts(LOD_in,keygone):
    * This function reads in a list of dicts and subsets it
    * It removes key:value pairs specified by keys in keygone
* DictlistToStringlist(dictlist_in):
    * This function reads in a list of dicts 
    * It iterates through each value and appends it to a list
    * Outputs a list of strings
* StringToDate_ManyFormats(str_in,list_of_formats = ["%m/%d/%Y %H:%M:%S %p"] ):
    * Given a list_of_formats (datetime.datetime formats), this function reads in a string and tries to return it as one of those datetime formats
    * It also strips commas because there was one format in excel that did not exist in strptime (Wednesday, March 14, 2012) -- note two commas
    * It also considers numeric input by using time.ctime()
* ReadValue_ManyFormats(str_in):
    * This funciton reads in a string and tries to convert it to an integer
    * It assumes that the input is human-readable as a number
    * It accepts scientific notation and percents, and returns zero if not a number or blank

