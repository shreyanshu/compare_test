"""
Comparing cols using xls files
"""
import pymysql
import pandas as pd
import math
"""
file location
"""
col_file = pd.read_excel('C:\\Users\\Goldy\\Desktop\\columns.xlsx')
print(col_file)
table1_cols = col_file.iloc[0]['source_col']
table2_cols = col_file.iloc[0]['target_col']
"""
getting list of column names
"""
# print(table1_cols.replace(" ",'').split(','))
#
"""
conn to db
"""
conn = pymysql.connect(user='root', password='', db='compare_test')
df_db_1 = pd.read_sql('select ' + table1_cols +' from test_table', conn)
df_db_2 = pd.read_sql('select ' + table2_cols + ' from test_table_2', conn)

df_db_2.columns = table1_cols.replace(" ",'').split(',')

"""
adding extra cols
"""
df_db_1['Table']='Table 1'
df_db_2['Table']='Table 2'

"""merger to find duplicates"""
df_compare = df_db_1.merge(df_db_2, on=table1_cols.replace(" ",'').split(','), how='outer')
# print(df_compare)
"""getting mismatch rows"""
df_compare = df_compare.loc[(df_compare['Table_x'].isnull()) | (df_compare['Table_y'].isnull())]
#
"""generating final `table` column"""
df_compare['Table'] = df_compare.apply(lambda x: x['Table_y'] if pd.notnull(x['Table_y']) else x['Table_x'], axis=1)
"""dropping columns that are not required"""
df_compare = df_compare.drop(['Table_x', 'Table_y'], axis=1)
"""write to csv"""
df_compare.to_excel('C:\\Users\\Goldy\\Desktop\\result.xlsx', index=False)
