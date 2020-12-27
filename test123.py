
import pandas as pd

try:
    df_csv = pd.read_csv('C:\\Users\\Goldy\\Desktop\\data_csv.csv')
    print(df_csv)
except:
    print("Cant parse csv")