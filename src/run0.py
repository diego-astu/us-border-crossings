#!/usr/bin/python3
import csv
import os
import operator
import itertools
import datetime

path = os.path.join(os.getcwd(), '../input/small_Border_Crossing_Entry_Data.csv')

"""For the purposes of this challenge, you'll want to pay attention to the following fields:
Border: Designates what border was crossed
Date: Timestamp indicating month and year osf crossing
Measure: Indicates means, or type, of crossing being measured (e.g., vehicle, equipment, passenger or pedestrian)
Value: Number of crossings
"""
keepvars = ['Border','Date','Measure','Value']
indat0 = []

with open(path) as csvfile:
    reader = csv.DictReader(csvfile, 
    	fieldnames=('Port Name','State','Port Code','Border','Date','Measure','Value','Location'))
    next(reader)
    for row in reader:
    	row['Value'] = int(row['Value'])
    	row['Date'] = datetime.datetime.strptime(row['Date'], "%d/%m/%Y %H:%M:%S %p")

    	indat0.append({ your_key: row[your_key] for your_key in keepvars })
print(indat0)

print("SORTED")
"""indat1 = sorted(indat0, key = lambda x: (x[0], x[1]))"""
indat1 = sorted(indat0, key=operator.itemgetter('Border', 'Date','Measure'))
print(indat1)
print("GROUPED")

host_data = []
for k,v in itertools.groupby(indat1, key=lambda x:(x['Border'], x['Date'], x['Measure'])):
   
   host_data.append({'grouping':k, 'sum':sum(int(row['Value']) for row in v)})

print(host_data)
