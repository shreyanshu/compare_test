import pandas as pd
import pymysql
from sqlalchemy import create_engine
from sqlalchemy.dialects.oracle import VARCHAR

conn = pymysql.connect(user='root', password='', db='compare_test')
df_src = pd.read_sql("select * from test_table", conn)


con2 = create_engine('mysql+pymysql://root:@localhost/compare_test_copy')
# oracle+cx_oracle://user:pass@host:port/dbname
cols = df_src.dtypes[df_src.dtypes == 'object'].index
type_mapping = {col: VARCHAR(255) for col in cols}
df_src.to_sql('inventory', con2, dtype=type_mapping, schema='', index=False,
              if_exists='replace')

# df_src.to_sql('test_target_table', con2, schema='', index=False)
# df_src.to_sql('test_target_table', conn2, schema='')
