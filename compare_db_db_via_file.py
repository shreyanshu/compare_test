import pandas as pd

import pymysql

conn = pymysql.connect(user='root', password='', db='compare_test')
# df_control = pd.read_sql("select columns from control_table", conn)
# cols_to_compare = list(df_control['columns'])

where_target = "age = 12"
df = pd.read_excel('C:\\Users\\Goldy\\Desktop\\control_file.xlsx')

query = df.loc[0]['filter']
target_schema = df.loc[0]['target_schema']
target_table_name = df.loc[0]['target_table_name']

df_table = pd.read_sql(query, conn)

# query_target = 'select ' + ', '.join(df['target_cols']) + ' from ' + target_schema + '.' + target_table_name
query_target = 'select ' + ', '.join(df['target_cols']) + ' from ' + target_table_name
if where_target != '':
    query_target = query_target + ' where ' + where_target

df_table_2 = pd.read_sql(query_target, conn)
