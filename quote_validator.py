import pandas as pd
import csv
df = pd.read_csv('C:\\Users\\Goldy\\Desktop\\data_csv.csv',
                 quoting=3)
# print(df)
mask = df.apply(lambda x: x.astype(str).str.match('^"[^"]*"$').all(), axis=1)
df_invalid = df[~mask]
print(df_invalid)