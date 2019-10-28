#!/usr/bin/python3
import csv
import os
 
dirpath = os.getcwd()
print("current directory is : " + dirpath)


with open(os.path.join(dirpath, '../input/small_Border_Crossing_Entry_Data.csv')) as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        print(row)
        