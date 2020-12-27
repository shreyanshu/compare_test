import pandas as pd
import pymysql

conn = pymysql.connect(user='root', password='', db='compare_test')
writer = pd.ExcelWriter('info.xlsx', engine='xlsxwriter')

col_file = pd.read_excel('C:\\Users\\Goldy\\Desktop\\columns.xlsx')
db_cols = col_file.iloc[0]['source_col']
"""Converting user specified cols to lower case"""
csv_cols = col_file.iloc[0]['target_col'].lower()

csv_cols_list = [x[1:] if x[0] is " " else x for x in csv_cols.split(',')]
# csv_cols_list = csv_cols.replace(" ", '').split(',')
print(csv_cols_list)
df_csv = pd.read_csv('C:\\Users\\Goldy\\Desktop\\data_csv.csv')
"""Converting all columns to lower case (file and csv only)"""
df_csv.columns = df_csv.columns.str.lower()
df_csv = df_csv[csv_cols_list]

"""dropping duplicates from csv df"""
# df_csv = df_csv.drop_duplicates()

df_db = pd.read_sql('select '+db_cols+' from test_table', conn)
df_db.columns = csv_cols_list
null_counts_table = df_db.isnull().sum()

count_list=[]
count_list.append({'Table': 'DB', 'Count': df_db.shape[0]})
count_list.append({'Table': 'CSV', 'Count': df_csv.shape[0]})
pd.DataFrame(count_list).to_excel(writer, sheet_name='Count Validation', index=False)

"""Changes all NULL to Nan"""
df_db = df_db.replace({'NULL': None})

"""Getting counts of null values in CSV"""
null_counts_csv = df_csv.isnull().sum()

pd.DataFrame({'Columns': null_counts_csv.index,
              'Null Count CSV': null_counts_csv,
              'Null Count DB': null_counts_table}).to_excel(writer, sheet_name='Null Count Validation', index=False)

"""Duplicate Counts"""
df_duplicate_table = pd.read_sql("select " + db_cols+ ", count(*) from test_table group by "+db_cols, conn)
df_dup_csv = df_csv.groupby(csv_cols_list, dropna=False).size()
df_dup_csv = df_dup_csv.loc[df_dup_csv>1].reset_index(name='count(*)')
df_duplicate_table = df_duplicate_table.loc[df_duplicate_table['count(*)']>1]
db_col_list = [x[1:] if x[0] is " " else x for x in db_cols.split(',')]
df_duplicate_table = df_duplicate_table.rename(dict(zip(db_col_list, csv_cols_list)), axis=1)
df_duplicate_table['TABLE'] = 'TABLE'
df_dup_csv['TABLE'] = 'CSV'
df_duplicate_table = df_duplicate_table.append(df_dup_csv)
cols = df_duplicate_table.columns
cols = [cols[-1]] + list(cols[:-1])
df_duplicate_table = df_duplicate_table[cols]
df_duplicate_table.to_excel(writer, sheet_name='Duplicate Validation', index=False)
"""
Converting possible cols to datetime
"""
from pandas.api.types import is_datetime64_any_dtype
import numpy as np


for col in df_db.columns:
    if df_db[col].dtype=='object' or is_datetime64_any_dtype(df_db[col]):
        try:
            """checking if the csv column is in int format"""
            if df_csv[col].dtype == np.int64:
                df_db[col] = pd.to_datetime(df_db[col], format='%Y-%m-%d')
                df_csv[col] = pd.to_datetime(df_csv[col], format='%Y%m%d')
            else:
                df_db[col] = pd.to_datetime(df_db[col], format='%Y-%m-%d')
                df_csv[col] = pd.to_datetime(df_csv[col])
        except:
            print(col, 'not converted to date time')
# df_db['dob'] = pd.datetime(df_db['dob'])



for col in df_db.columns:
    if df_db[col].dtype is not df_csv[col].dtype:
        if df_csv[col].dtype in [int, float] or df_db[col].dtype in [int, float]:
            df_db[col] = df_db[col].astype(float)
            df_csv[col] = df_csv[col].astype(float)
        else:
            df_db[col] = df_db[col].astype(str)
            df_csv[col] = df_csv[col].astype(str)
    else:
        print("dtype of", col, "Matched")
        if df_csv[col].dtype == object:
            """Remove whitespaces from CSV df"""
            df_csv[col] = df_csv[col].str.lstrip()
            df_csv[col] = df_csv[col].str.rstrip()
            """Remove whitespaces from DB df"""
            df_db[col] = df_db[col].str.lstrip()
            df_db[col] = df_db[col].str.rstrip()
            print('spaces removed from', col)
# print(df_db.dtypes)
# print(df_csv.dtypes)

df_db['Table'] = 'Database'
df_csv['Table'] = 'CSV File'

# print(df_csv.loc[df_csv['full_name'] == 'ram'])

df_compare = df_db.merge(df_csv, on=csv_cols_list, how='outer')
df_compare = df_compare.loc[(df_compare['Table_x'].isnull()) | df_compare['Table_y'].isnull()]
# print(df_compare.loc[df_compare['full_name'] == 'ram'])
if df_compare.shape[0] == 0:
    df_compare = df_compare.drop(['Table_x', 'Table_y'], axis=1)
    df_compare.to_excel(writer, sheet_name='Data Validation', index=False)
else:
    df_compare['Table'] = df_compare.apply(lambda x: x['Table_y'] if pd.notnull(x['Table_y']) else x['Table_x'], axis=1)
    df_compare = df_compare.drop(['Table_x', 'Table_y'], axis=1)
    columns = df_compare.columns
    columns = [columns[-1]] + list(columns[:-1])
    df_compare = df_compare[columns]
    df_compare.to_excel(writer, sheet_name='Data Validation', index=False)
