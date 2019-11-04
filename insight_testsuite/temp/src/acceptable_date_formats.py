#!/usr/bin/python3
###########################
###########################
#
# This script produces a list called final_list_of_datetime_strings
#  which contains all datetime formats I can accept 
# These formats come from producing combinations of all
#  date formats seen in Excel (en_US locale)
# One of my helper functions will loop through all of these formats
#  when reading in date field
###########################
###########################

######################################################
#There are only a few ways to express hour:minute:second
######################################################
hms_combinations = [
{'hour': '%H:', 'minute': '%M:', 'second': '%S', 'AMPM': ' %p'}, 
{'hour': '%H:', 'minute': '%M:', 'second': '%S'}, 
{'hour': '%I:', 'minute': '%M:', 'second': '%S'}
]
#Its also possible to express hour:minute without seconds
hm_combinations = [
{'hour': '%H:', 'minute': '%M:', 'AMPM': ' %p'}, 
{'hour': '%H:', 'minute': '%M:'}, 
{'hour': '%I:', 'minute': '%M:'}
]
######################################################
#its a little more complicated for month/day/year
######################################################
possible_day_formats = ['%d']
possible_month_formats = ['%b','%B', '%m']
possible_year_formats = ['%y', '%Y']
possible_weekday_formats = ['%a','%A']
# out of those lists create dicts (dicts are ordered in py3)
# each dict is a possible ordering of the possible formats
# we will call these components
mdy_components = {
	'month' : possible_month_formats,
	'day' : possible_day_formats,
	'year' : possible_year_formats}
ymd_components = {
	'year' : possible_year_formats,
	'month' : possible_month_formats,
	'day' : possible_day_formats
	}
dmy_components = {
	'day' : possible_day_formats,
	'month' : ['%b','%B'], ## day can appear before month only when month is spelled
	'year' : possible_year_formats,
}
#As long as date doesnt start with a year, it can be led by a weekday
amdy_components = {
	'weekday': possible_weekday_formats,
	'month' : possible_month_formats,
	'day' : possible_day_formats,
	'year' : possible_year_formats}
admy_components = {
	'weekday': possible_weekday_formats,
	'day' : possible_day_formats,
	'month' : ['%b','%B'], ## day can appear before month only when month is spelled
	'year' : possible_year_formats,
}

#START COMBINING DAY MARKERS
amdy_combinations = CombineComponents(amdy_components)
admy_combinations = CombineComponents(admy_components)
#its possible to express monthyearday without weekday
mdy_combinations = CombineComponents(mdy_components)
ymd_combinations = CombineComponents(ymd_components)
dmy_combinations = CombineComponents(dmy_components)
#its possible to express monthyear without day
my_combinations = RemoveKeysListofDicts(mdy_combinations, 'day')
ym_combinations = RemoveKeysListofDicts(ymd_combinations, 'day')
my_combinations = RemoveKeysListofDicts(dmy_combinations, 'day')


######################################################
#Append all combinations into one big list per grouping
######################################################
dictlist_all_time_combinations = hms_combinations + hm_combinations
dictlist_all_date_combinations = amdy_combinations + admy_combinations + mdy_combinations + ymd_combinations + dmy_combinations + my_combinations + ym_combinations + my_combinations

######################################################
#Convert from dictlist to string list, and make some final modifications
######################################################
#time is optional so add blank +[''] so that we can combine Date formats with the absence of time
list_of_all_time_combinations = DictlistToStringlist(dictlist_all_time_combinations) + [''] 

#Currently dates are separated by % but we also need a slash at the front
#But the first character in a date string cannot be a slash so exclude first character using [1:]
list_of_all_date_combinations = [element.replace('%','/%')[1:] for element in DictlistToStringlist(dictlist_all_date_combinations)]

#For date, allow separator to also be a space
list_of_all_date_combinations_space = [element.replace('/',' ') for element in list_of_all_date_combinations]

#All times must be preceded by a space so that there is a separator between date & time
#Dont allow for trailing/leading colons
final_all_times = [ f' {x}'.replace(': %p', ' %p').strip(':') for x in list_of_all_time_combinations ]
final_all_dates = list_of_all_date_combinations + list_of_all_date_combinations_space


list_of_recognized_datetime_formats = list(itertools.product(final_all_dates, final_all_times))

#For speed, first entry will be the default input
final_list_of_datetime_strings = ["%m/%d/%Y %H:%M:%S %p"] 
#Append all other formats after this. its okay that there will be a duplicate
for t in list_of_recognized_datetime_formats:
	string_out = ''
	for v in t:
		string_out = CleanWhitespace(string_out + v + str(''))
		#print(string_out)
	final_list_of_datetime_strings.append(string_out)


