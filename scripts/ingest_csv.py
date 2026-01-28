import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from db_connection import engine
from clean import clean_data
 
CSV_PATH = "data.csv"
TABLE_NAME = "orders02"
 
df = pd.read_csv(CSV_PATH)
df = clean_data(df)
 
df.to_sql(TABLE_NAME, engine, if_exists="replace", index=False)
 
print("CSV cleaned and ingested successfully")
 