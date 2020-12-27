import pandas as pd
import pymysql

conn = pymysql.connect(user='root', password='', db='compare_test')

df_db_src = pd.read_sql('select distinct name, age, dob from test_table', conn)
df_db_tar = pd.read_sql('select distinct name, age, dob from test_table_2', conn)

'''Getting rows with special symbols'''
mask = df_db_tar.apply(lambda x: x.astype(str).str.match('^[\s.a-zA-Z0-9-,&]*$').all(), axis=1)
df_invalid = df_db_tar.loc[~mask]
df_invalid.to_excel('Invalid_records.xlsx', index=False)
# """"""
# df_db_src = df_db_src.drop_duplicates()
# df_db_tar = df_db_tar.drop_duplicates()

# df_db_tar.columns = df_db_src.columns
df_db_src_cols = df_db_src.columns
df_db_tar.columns = df_db_src_cols

# from pandas.api.types import is_datetime64_any_dtype
# for col in df_db_src.columns:
#     if df_db_src[col].dtype == 'object' or is_datetime64_any_dtype(df_db_src[col]):
#         try:
#             df_db_src[col] = pd.to_datetime(df_db_src[col])
#             df_db_tar[col] = pd.to_datetime(df_db_tar[col])
#         except:
#             print(col, 'not converted to date time')
#             pass
# print(df_csv.dtypes)
# print(df_table.dtypes)
df_db_tar['Table'] = 'Target CSV'
df_db_src['Table'] = 'Source CSV'

df_compare = df_db_src.merge(df_db_tar, on=list(df_db_src_cols), how='outer')
# print(df_compare)
df_compare = df_compare.loc[(df_compare['Table_x'].isnull()) | df_compare['Table_y'].isnull()]
df_compare['Table'] = df_compare.apply(lambda x: x['Table_y'] if pd.notnull(x['Table_y']) else x['Table_x'], axis=1)
df_compare = df_compare.drop(['Table_x', 'Table_y'], axis=1)
df_compare.to_excel('result_db_db.xlsx', index=False)

