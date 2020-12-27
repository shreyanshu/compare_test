import pymysql
import pandas as pd
import math

"""
making a conn to the db
"""
conn = pymysql.connect(user='root', password='', db='compare_test')
"""
Change table names
"""
df_db_1 = pd.read_sql('select * from test_table', conn)
df_db_2 = pd.read_sql('select * from test_table_2', conn)
col_names = df_db_2.columns
# print(df_db_1.shape)
# print(df_db_2.shape)
print('Row difference:', math.fabs(df_db_1.shape[0]-df_db_2.shape[0]))
df_db_1['table'] = "Table 1"
df_db_2['table'] = "Table 2"

df_concat = pd.concat([df_db_1, df_db_2], ignore_index=True)
# print(df_concat)
df_compare = df_concat.drop_duplicates(subset=col_names,keep=False)
df_compare.to_csv('result.csv', sep=',', index=False)