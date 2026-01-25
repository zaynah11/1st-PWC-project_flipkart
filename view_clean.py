import pandas as pd
from db_connection import engine

df = pd.read_sql("select * from orders", engine)
print(df.head())