from sqlalchemy import create_engine, MetaData, Table
import json
import string
import pandas as pd
import seaborn
import matplotlib.pyplot as plt
import re

def return_video_number(x):
	x.encode("utf-8")
	re.sub("\D", "", x)
	print(x)
	return x

def transform_worker_ids(df):
	df['uniqueid'] = pd.factorize(df.uniqueid)[0] + 1

def transform_video_names(df):
	for i in range(len(df['clip'])):
		return_video_number(df['clip'][i])


def analyze(database_file):
	db_url = "sqlite:///../../data/"+database_file+".db"
	table_name = 'moral_dynamics'
	data_column_name = 'datastring'
	engine = create_engine(db_url)
	metadata = MetaData()
	metadata.bind = engine
	table = Table(table_name, metadata, autoload=True)
	# make a query and loop through
	s = table.select()
	rows = s.execute()
	data = []
	#status codes of subjects who completed experiment
	statuses = [3,4,5]
	# if you have workers you wish to exclude, add them here
	exclude = ['debug']
	for row in rows:
	    # Only use subjects who completed experiment and aren't excluded
	    if (row['status'] in statuses and row['uniqueid'] not in exclude 
	    	and row['codeversion'] == 'experiment_1'):
	        data.append(row[data_column_name])
	# Parse each participant's datastring as json object
	data = [json.loads(part)['data'] for part in data]
	for part in data:
	    for record in part:
	        record['trialdata']['uniqueid'] = record['uniqueid']

	# Flatten nested list so we just have a list of the trialdata recorded
	data = [record['trialdata'] for part in data for record in part]
	df = pd.DataFrame(data)
	transform_worker_ids(df)
	transform_video_names(df)
	print(df)

analyze('experiment1')