import sqlite3

# begin SQL connection and set cursor
conn = sqlite3.connect('participants.db')
cursor = conn.cursor()

# declare list and dictionary of data from SQL db
dataList = []
dataDict = {}

# traverse SQL database and grab the data
for row in cursor.execute("SELECT * FROM moral_dynamics WHERE datastring!='NULL'"):
	# begin string
	string = row[16]

	# find data begin in string and extract rest of string
	index = string.index('"data"')
	newString = string[index:]

	# split the string by commas
	for str in newString.split(','):
		# if "clip" or "rating", extract and add to list
		if "clip" in str:
			dataList.append(str[26:-1]) # clean extraction
		if "rating" in str:
			str2 = str[9:-2] # clean extraction
			if "}" in str2:
				str = str2[:-1]
			else:
				str = str2
			dataList.append(str)

# add the datapoints to dictionary
for i in range(len(dataList)):
	if i%2 == 0:
		dataDict.setdefault(int(dataList[i]),[]).append(int(dataList[i+1]))