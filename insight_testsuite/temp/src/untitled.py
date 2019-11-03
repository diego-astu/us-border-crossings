import datetime

print(datetime.datetime.strptime('03/01/2019 3:00AM', '%m/%d/%Y %I:%M%p'))
print(datetime.datetime.strptime('3/1/19 3:00AM', '%m/%d/%y %I:%M%p'))
print(datetime.datetime.strptime('Wednesday March 14 2012', '%A %B %d %Y'))