import pandas as pd
import numpy as np
import pymysql

conn = pymysql.connect(user='root', password='', db='compare_test')
df_control = pd.read_sql("select columns from control_table", conn)
cols_to_compare = list(df_control['columns'])
# print(cols_to_compare)

"""
If we have to hard code the columns we 
"""

# cols_to_exclude = ['roll', 'name']
# for col in cols_to_exclude:
#     cols_to_compare.remove(col)

df_info = pd.read_csv('info.csv', header=None)

df_info = df_info.replace({None: ''}).set_index(0)
owner1 = df_info.loc['owner1'][1]
table1 = df_info.loc['table1'][1]
where1 = df_info.loc['where1'][1]

owner2 = df_info.loc['owner2'][1]
table2 = df_info.loc['table2'][1]
where2 = df_info.loc['where2'][1]


query1 = "select " + ",".join(cols_to_compare) + ' from '+ owner1 + "."+ table1
if where1!="" and not pd.isnull(where1):
    query1 = query1 + " where " + where1
df_table1 = pd.read_sql(query1, conn)

"""Replacing NULL with nans (empty value)"""
if object in df_table1.dtypes:
    df_table1.replace({"NULL": np.nan}, inplace=True)

"""query for duplicates"""
if where1!="":
    query_dup1 = "select " + ",".join(cols_to_compare) + ", count(*) from "+table1+" where "+where1+" group by "+",".join(cols_to_compare)
else:
    query_dup1 = "select " + ",".join(
        cols_to_compare) + ", count(*) from " + table1 + " group by " + ",".join(cols_to_compare)
df_duplicate_table1 = pd.read_sql(query_dup1, conn)
df_duplicate_table1 = df_duplicate_table1.loc[df_duplicate_table1['count(*)']>1]
df_duplicate_table1['Table'] = 'Table 1'

"""Get null values in table 1"""
null_counts_table1 = df_table1.isnull().sum()

"""Query for table 2"""
query2 = "select " + ",".join(cols_to_compare) + ' from '+owner2+'.'+ table2
if where2!="":
    query2 = query2 + " where " + where2

df_table2 = pd.read_sql(query2, conn)
"""Replacing NULL with NAN(empty value)"""
if object in df_table2.dtypes:
    df_table2.replace({"NULL": np.nan}, inplace=True)

"""Query for duplicates in table 2"""
if where2!="":
    query_dup2 = "select " + ",".join(cols_to_compare) + ", count(*) from "+table2+" where "+where2+" group by "+",".join(cols_to_compare)
else:
    query_dup2 = "select " + ",".join(
        cols_to_compare) + ", count(*) from " + table2 + " group by " + ",".join(cols_to_compare)
df_duplicate_table2 = pd.read_sql(query_dup2, conn)
df_duplicate_table2 = df_duplicate_table2.loc[df_duplicate_table2['count(*)']>1]
df_duplicate_table2['Table'] = 'Table 2'

"""Making the final duplicate df"""
df_dup = df_duplicate_table1.append(df_duplicate_table2)
df_dup.replace({"None": np.nan}, inplace=True)
"""Saving the file"""
df_dup.to_excel('duplicates.xlsx', index=False)

"""Get null values in table 1"""
null_counts_table2 = df_table2.isnull().sum()

"""Making a df with null value counts of all columns of both tables"""
df_null_counts = pd.DataFrame({
    "col_name":null_counts_table1.index,
    "null_count_table1": null_counts_table1.values,
    "null_count_table2": null_counts_table2.values})
"""Saving the null count file"""
df_null_counts.to_excel('null_counts.xlsx', index=False)

"""Compare logic"""
df_table1['Table'] = table1 + ' - ' + table2
df_table2['Table'] = table2 + ' - ' + table1

"""Handling type mismatches in pandas"""
for col in df_table1.columns:
    if df_table1[col].dtype == df_table2[col].dtype:
        print(col, "dtype Matched")
    else:
        print(col, "dtype Mismatch")
        if df_table1[col].dtype in [np.int64, np.float64] or df_table2[col].dtype in [np.int64, np.float64]:
            df_table2[col] = df_table2[col].astype(float)
            df_table1[col] = df_table1[col].astype(float)
        else:
            df_table2[col] = df_table2[col].astype(str)
            df_table1[col] = df_table1[col].astype(str)

"""Merge operation"""
df_compare = df_table1.merge(df_table2, on=cols_to_compare, how='outer')
df_compare = df_compare.loc[(df_compare['Table_x'].isnull()) | df_compare['Table_y'].isnull()]
"""saving the final result"""
if df_compare.shape[0] == 0:
    """all mismatched rows"""
    # df_compare = df_compare.drop(['Table_x', 'Table_y'], axis=1)
    # df_compare.to_excel('result_csv_db.xlsx', index=False)
    df_compare = pd.DataFrame({"column_name": cols_to_compare, "status":"Match"})
    df_compare.to_excel('result_db_db_control_col.xlsx', index=False)
else:
    df_compare['Table'] = df_compare.apply(lambda x: x['Table_y'] if pd.notnull(x['Table_y']) else x['Table_x'], axis=1)
    df_compare = df_compare.drop(['Table_x', 'Table_y'], axis=1)
    columns = df_compare.columns
    columns = [columns[-1]] + list(columns[:-1])
    df_compare = df_compare[columns]
    df_compare.to_excel('result_db_db_control_col.xlsx', index=False)



