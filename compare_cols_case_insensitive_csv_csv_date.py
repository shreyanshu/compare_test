import  pandas as pd

col_file = pd.read_excel('C:\\Users\\Goldy\\Desktop\\columns.xlsx')
csv_source_cols = col_file.iloc[0]['source_col'].lower()
"""Converting user specified cols to lower case"""
csv_target_cols = col_file.iloc[0]['target_col'].lower()

csv_source_cols_list = csv_source_cols.replace(" ",'').split(',')
csv_target_cols_list = csv_target_cols.replace(" ",'').split(',')
df_csv_src = pd.read_csv('C:\\Users\\Goldy\\Desktop\\train_src.csv')
"""Converting all columns to lower case (file and csv only)"""
df_csv_src.columns = df_csv_src.columns.str.lower()
df_csv_src = df_csv_src[csv_source_cols_list]
df_csv_src = df_csv_src.drop_duplicates()

df_csv_tar = pd.read_csv('C:\\Users\\Goldy\\Desktop\\train_tar.csv')
"""Converting all columns to lower case (file and csv only)"""
df_csv_tar.columns = df_csv_tar.columns.str.lower()
df_csv_tar = df_csv_tar[csv_target_cols_list]
df_csv_tar = df_csv_tar.drop_duplicates()
df_csv_tar.columns = csv_source_cols_list

for col in df_csv_tar.columns:
    if df_csv_tar[col].dtype == 'object':
        try:
            df_csv_tar[col] = pd.to_datetime(df_csv_tar[col])
            df_csv_src[col] = pd.to_datetime(df_csv_src[col])
        except:
            print(col, 'not converted to datetime')

df_csv_src['Table'] = 'Source CSV'
df_csv_tar['Table'] = 'Target CSV'

df_compare = df_csv_src.merge(df_csv_tar, on=csv_source_cols_list, how='outer')
df_compare = df_compare.loc[(df_compare['Table_x'].isnull()) | df_compare['Table_y'].isnull()]

if df_compare.shape[0]==0:
    df_compare = df_compare.drop(['Table_x', 'Table_y'], axis=1)
    df_compare.to_excel('result_csv_csv.xlsx', index=False)
else:
    df_compare['Table'] = df_compare.apply(lambda x: x['Table_y'] if pd.notnull(x['Table_y']) else x['Table_x'], axis=1)
    df_compare = df_compare.drop(['Table_x', 'Table_y'], axis=1)
    df_compare.to_excel('result_csv_csv.xlsx', index=False)



