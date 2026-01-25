import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
 
import pandas as pd
from db_connection import engine
 
TABLE_NAME = "orders"   # change if your table name is different
OUT_DIR = "reports"
os.makedirs(OUT_DIR, exist_ok=True)
 
df = pd.read_sql(f'SELECT * FROM "{TABLE_NAME}"', engine)
 
# 1) basic shape
shape = {"rows": len(df), "cols": len(df.columns)}
 
# 2) missing %
missing_pct = (df.isna().mean() * 100).round(2).sort_values(ascending=False)
 
# 3) duplicate rows
dup_rows = int(df.duplicated().sum())
 
# 4) column-wise unique counts
unique_counts = df.nunique(dropna=True).sort_values(ascending=False)
 
# 5) basic type info
dtypes = df.dtypes.astype(str)
 
# 6) numeric sanity (min/max/mean)
num = df.select_dtypes(include="number")
num_summary = num.describe().T if not num.empty else pd.DataFrame()
 
# ---- Save outputs ----
missing_pct.to_csv(f"{OUT_DIR}/missing_percent.csv", header=["missing_percent"])
unique_counts.to_csv(f"{OUT_DIR}/unique_counts.csv", header=["unique_count"])
dtypes.to_csv(f"{OUT_DIR}/dtypes.csv", header=["dtype"])
if not num_summary.empty:
    num_summary.to_csv(f"{OUT_DIR}/numeric_summary.csv")
 
# ---- Print quick report ----
print("=== DB CHECKS ===")
print("Table:", TABLE_NAME)
print("Rows:", shape["rows"], "Cols:", shape["cols"])
print("Duplicate rows:", dup_rows)
print("\nTop 10 missing% columns:")
print(missing_pct.head(10))
print("\nSaved reports/ -> missing_percent.csv, unique_counts.csv, dtypes.csv, numeric_summary.csv (if numeric)")