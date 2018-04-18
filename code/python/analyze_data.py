'''
Set of methods for analyzing experiment and model data
for Moral Dynamics.

Felix Sosa
'''

import pandas as pd
import sqlite3

# Variables containing db paths
experiment_1_db = '../../data/experiment1.db'
experiment_2_db = '../../data/experiment2.db'
experiment_3_db = '../../data/experiment3.db'
experiment_4_db = '../../data/experiment4.db'

# Extract data into dataframes
conn_1 = sqlite3.connect(experiment_1_db)
df_1 = pd.read_sql_query("select * from moral_dynamics WHERE status BETWEEN 3 AND 5 \
						  AND uniqueid NOT IN ('debug');", conn_1)

conn_2 = sqlite3.connect(experiment_2_db)
df_2 = pd.read_sql_query("select * from moral_dynamics WHERE status BETWEEN 3 AND 5 \
						  AND uniqueid NOT IN ('debug');", conn_2)

conn_3 = sqlite3.connect(experiment_3_db)
df_3 = pd.read_sql_query("select * from moral_dynamics WHERE status BETWEEN 3 AND 5 \
						  AND uniqueid NOT IN ('debug');", conn_3)

conn_4 = sqlite3.connect(experiment_4_db)
df_4 = pd.read_sql_query("select * from moral_dynamics WHERE status BETWEEN 3 AND 5 \
						  AND uniqueid NOT IN ('debug');", conn_4)
