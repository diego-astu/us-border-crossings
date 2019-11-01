

a = [ 


 {'Date': 'blue', 
'Border': 'US-Mexico Border', 
'Value': 346158.0,
 'Measure': 'Pedestrians'},
{'Date': '03/01/2019 12:00:00 AM', 
'Border': 'US-Mexico Border', 
'Value': 346158.0,
 'Measure': 'Pedestrians'},

]

def in_dictlist((key, value), my_dictlist):
    for dict_i in my_dictlist:
    	#print(dict_i)
        #if dict_i[key] == value:
        if any(dict_i[key] == value for dict_i in my_dictlist):
            return my_dictlist
        else:
        	dict_j = dict_i.copy()
        	dict_j[key] = value
        	dict_j['Value'] = 0.0
        	ReturnsNone = my_dictlist.extend([dict(dict_j)])
        	return my_dictlist

print in_dictlist(('Date','orange'), a)

b = []
for colors in ['red','lskjdf','sldkfjas','lksjdfla']:
	print(colors)
	b = in_dictlist(('Date',colors), a)

print(b)