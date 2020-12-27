import pandas as pd
import pymysql

conn = pymysql.connect(user='root', password='', db='compare_test')

col_file = pd.read_excel('C:\\Users\\Goldy\\Desktop\\columns.xlsx')
db_cols = col_file.iloc[0]['source_col']
csv_cols = col_file.iloc[0]['target_col']

csv_cols_list = csv_cols.replace(" ",'').split(',')

df_csv = pd.read_csv('C:\\Users\\Goldy\\Desktop\\data_csv.csv', usecols=csv_cols_list)

"""dropping duplicates from csv df"""
df_csv = df_csv.drop_duplicates()

df_db = pd.read_sql('select '+db_cols+' from test_table', conn)
df_db.columns = csv_cols_list

df_db['Table'] = 'Database'
df_csv['Table'] = 'CSV File'

df_compare = df_db.merge(df_csv, on=csv_cols_list, how='outer')
df_compare = df_compare.loc[(df_compare['Table_x'].isnull()) | df_compare['Table_y'].isnull()]
df_compare['Table'] = df_compare.apply(lambda x: x['Table_y'] if pd.notnull(x['Table_y']) else x['Table_x'], axis=1)
df_compare = df_compare.drop(['Table_x', 'Table_y'], axis=1)
df_compare.to_excel('result_csv_db.xlsx', index=False)
