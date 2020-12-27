import pymysql
import pandas as pd
import math

cols_to_compare = ['name', 'age']

conn = pymysql.connect(user='root', password='', db='compare_test')
df_db_1 = pd.read_sql('select * from test_table', conn)

df_db_2 = pd.read_sql('select * from test_table_2', conn)

df_db_1 = df_db_1[cols_to_compare]
df_db_2 = df_db_2[cols_to_compare]

df_db_1['Table']='Table 1'
df_db_2['Table']='Table 2'

# df_compare = pd.concat([df_db_1,df_db_2], ignore_index=True).drop_duplicates(subset=cols_to_compare,keep=False)
# df_compare.to_csv('results_cols.csv', sep=',', index=False)

# Join in python
df_compare = df_db_1.merge(df_db_2, on=cols_to_compare, how='outer')
# print(df_compare)
df_compare = df_compare.loc[(df_compare['Table_x'].isnull()) | (df_compare['Table_y'].isnull())]

import numpy as np
df_compare['Table'] = df_compare.apply(lambda x: x['Table_y'] if pd.notnull(x['Table_y']) else x['Table_x'], axis=1)
df_compare = df_compare.drop(['Table_x', 'Table_y'], axis=1)
df_compare.to_csv('result_cols.csv', sep=',', index=False)
