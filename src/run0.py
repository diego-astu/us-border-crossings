#!/usr/bin/python3
import csv

with open('/Users/jdastu/Documents/GitHub/de-challenge-oct28/insight_testsuite/tests/test1/input/Border_Crossing_Entry_Data.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        print(row)
        print(row[0])
        print(row[0],row[1],row[2],)