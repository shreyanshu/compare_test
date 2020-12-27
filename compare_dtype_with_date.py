import pandas as pd
import pymysql

conn = pymysql.connect(user='root', password='', db='compare_test')

col_file = pd.read_excel('C:\\Users\\Goldy\\Desktop\\columns.xlsx')
db_cols = col_file.iloc[0]['source_col']
xlsx_cols = col_file.iloc[0]['target_col']

xlsx_cols_list = xlsx_cols.replace(" ",'').split(',') # name, age, roll

"""Source file location"""
df_xlsx = pd.read_excel('C:\\Users\\Goldy\\Desktop\\data.xlsx',
                        usecols=xlsx_cols_list, parse_dates=['dob'])

"""dropping duplicates from excel df"""
df_xlsx = df_xlsx.drop_duplicates()

df_db = pd.read_sql('select '+db_cols+' from test_table', conn)
print(df_db.dtypes)
# df_db['dob'] = pd.to_datetime(df_db['dob'])
# df_db.columns = xlsx_cols_list
#
# """dropping duplicates from db df"""
# df_db = df_db.drop_duplicates()
#
# df_db['Table'] = 'Database'
# df_xlsx['Table'] = 'File'
#
# print(df_db.dtypes)
# print(df_xlsx.dtypes)
#
# df_compare = df_db.merge(df_xlsx, on=xlsx_cols_list, how='outer')
# print(df_compare)
# df_compare = df_compare.loc[(df_compare['Table_x'].isnull()) | df_compare['Table_y'].isnull()]
# df_compare['Table'] = df_compare.apply(lambda x: x['Table_y'] if pd.notnull(x['Table_y']) else x['Table_x'], axis=1)
# df_compare = df_compare.drop(['Table_x', 'Table_y'], axis=1)
# df_compare.to_excel('result_file_db.xlsx', index=False)
