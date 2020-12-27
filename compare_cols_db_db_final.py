import pandas as pd
import pymysql

conn = pymysql.connect(user='root', password='', db='compare_test')
writer = pd.ExcelWriter('info.xlsx', engine='xlsxwriter')

df_db_src = pd.read_sql('select name, age, dob from test_table', conn)
df_db_tar = pd.read_sql('select name, age, dob from test_table_2', conn)

log_dir = {"Test Cases": [], "Status": []}

"""
null count
regular count
duplicate
compare
"""
"""Count"""
df_count = pd.DataFrame({'Table':['Source', 'Target'],
                         'Count':[df_db_src.shape[0], df_db_tar.shape[0]]})
log_dir['Test Cases'].append('Count Validation')
if df_count.loc[0, 'Count'] == df_count.loc[1, 'Count']:
    log_dir['Status'].append('Pass')
else:
    log_dir['Status'].append('Fail')

# """"""
# df_db_src = df_db_src.drop_duplicates()
# df_db_tar = df_db_tar.drop_duplicates()

# df_db_tar.columns = df_db_src.columns
"""Renaming the target df with columns of source df"""
df_db_src_cols = df_db_src.columns
df_db_tar.columns = df_db_src_cols

"""Null Values"""
null_val_src = df_db_src.isnull().sum()
null_val_tar = df_db_tar.isnull().sum()
df_null_count = pd.DataFrame({
    "Column": null_val_src.index,
    "Null Count Src": null_val_src.values,
    "Null Count Target": null_val_tar.values
})
"""Added for log generation"""
log_dir['Test Cases'].append('Null Count Validation')
if (null_val_src == null_val_tar).all():
    log_dir['Status'].append('Pass')
else:
    log_dir['Status'].append('Fail')

"""Duplicate"""
df_db_src_dup = df_db_src.groupby(list(df_db_src.columns), dropna=False).size().reset_index(name='count')
df_db_tar_dup = df_db_tar.groupby(list(df_db_tar.columns), dropna=False).size().reset_index(name='count')
df_db_src_dup['Table'] = 'Table 1'
df_db_tar_dup['Table'] = 'Table 2'
df_dup_final = df_db_src_dup.append(df_db_tar_dup)
columns = df_dup_final.columns
columns = [columns[-1]] + list(columns[:-1])
df_dup_final = df_dup_final[columns]
df_dup_final = df_dup_final.loc[df_dup_final['count']>1]
"""Added for log generation"""
log_dir['Test Cases'].append('Duplicate Count Validation')
if df_dup_final.shape[0] == 0:
    log_dir['Status'].append('Pass')
else:
    log_dir['Status'].append('Fail')

"""Comparision"""
df_db_tar['Table'] = 'Target CSV'
df_db_src['Table'] = 'Source CSV'

df_compare = df_db_src.merge(df_db_tar, on=list(df_db_src_cols), how='outer')
print(df_compare)
df_compare = df_compare.loc[(df_compare['Table_x'].isnull()) | df_compare['Table_y'].isnull()]

log_dir['Test Cases'].append('Data Validation')
if df_compare.shape[0] == 0:
    # df_compare = df_compare.drop(['Table_x', 'Table_y'], axis=1)
    df_compare = pd.DataFrame({'cols to compare':df_db_src_cols, "Status": "Match"})
    log_dir['Status'].append('Pass')
else:
    df_compare['Table'] = df_compare.apply(lambda x: x['Table_y'] if pd.notnull(x['Table_y']) else x['Table_x'], axis=1)
    df_compare = df_compare.drop(['Table_x', 'Table_y'], axis=1)
    columns = df_compare.columns
    columns = [columns[-1]] + list(columns[:-1])
    df_compare = df_compare[columns]
    log_dir['Status'].append('Fail')


# for i in range(4):
#     log_dir['Test Cases'].append("")
#     log_dir['Status'].append("")


# log_dir['Test Cases'].append("For details ....")
# log_dir['Status'].append(" ")


pd.DataFrame(log_dir).to_excel(writer, sheet_name='Log', index=False)
df_count.to_excel(writer, sheet_name='Count Validation', index=False)
df_null_count.to_excel(writer, sheet_name='Null Count Validation', index=False)
df_dup_final.to_excel(writer, sheet_name='Duplicate Count Validation', index=False)
df_compare.to_excel(writer, sheet_name='Data Validation', index=False)

wb = writer.book
ws = writer.sheets['Log']
bold = wb.add_format({'bold': True, "italic": True})
ws.write(10, 0, '**For Details look into the respective sheets', bold)
writer.save()















