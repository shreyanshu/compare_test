import pandas as pd

df_csv = pd.read_csv('C:\\Users\\Goldy\\Desktop\\data_csv.csv')
"""Converting all columns to lower case (file and csv only)"""
df_csv.columns = df_csv.columns.str.lower()
# print(df_csv)

"""primary key name"""
primary_key_name = 'id'
#
# df_csv['Record_Valid'] = df_csv.apply(lambda x: x.astype(str).str.match('^[a-zA-Z0-9-.#,\s\':_()/]*$').all(), axis=1)
# df_invalid_records = df_csv.loc[~df_csv['Record_Valid']]
# print(df_invalid_records)
# df_invalid_records.to_excel('invalid_records.xlsx', index=False)

"""make empty df for bad records"""
df_bad_records = pd.DataFrame()

"""Set primary key as the index"""
df_csv.set_index(primary_key_name, inplace=True)

"""iterate through all columns to find 'bad' records"""
for col in df_csv.columns:
    """get values that have bad values"""
    df_temp = df_csv[col][~df_csv[col].astype(str).str.match('^[a-zA-Z0-9-.#,\s\':_()/]*$')].reset_index()
    """rename the column name to value"""
    df_temp = df_temp.rename({col:'value'}, axis=1)
    """add the 'column' table"""
    df_temp['column'] = col
    """append to final df"""
    df_bad_records = df_bad_records.append(df_temp)


"""Change the order of columns"""
df_bad_records = df_bad_records[[primary_key_name]+['column', 'value']]

"""save the df"""
df_bad_records.to_excel('invalid_records.xlsx', index=False)
