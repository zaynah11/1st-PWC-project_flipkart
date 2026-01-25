import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
 
import pandas as pd
from db_connection import engine
 
TABLE_NAME = "orders"   # change if needed
OUT_DIR = "reports"
os.makedirs(OUT_DIR, exist_ok=True)
 
df = pd.read_sql(f'SELECT * FROM "{TABLE_NAME}"', engine)
 
def safe_mean(series):
    s = pd.to_numeric(series, errors="coerce")
    return float(s.mean()) if s.notna().any() else None
 
# --- Core metrics ---
insights = {}
 
insights["total_rows"] = int(len(df))
insights["total_columns"] = int(len(df.columns))
 
# CSAT
if "csat_score" in df.columns:
    csat = pd.to_numeric(df["csat_score"], errors="coerce")
    insights["avg_csat"] = round(float(csat.mean()), 3) if csat.notna().any() else None
    insights["median_csat"] = round(float(csat.median()), 3) if csat.notna().any() else None
 
# Sentiment distribution
if "sentiment" in df.columns:
    sentiment_counts = df["sentiment"].astype(str).value_counts(dropna=True).head(10)
    sentiment_counts.to_csv(f"{OUT_DIR}/sentiment_top.csv", header=["count"])
 
# Top reasons
if "reason" in df.columns:
    reason_counts = df["reason"].astype(str).value_counts(dropna=True).head(15)
    reason_counts.to_csv(f"{OUT_DIR}/top_reasons.csv", header=["count"])
 
# Top channels
if "channel" in df.columns:
    channel_counts = df["channel"].astype(str).value_counts(dropna=True)
    channel_counts.to_csv(f"{OUT_DIR}/channel_counts.csv", header=["count"])
 
# Call center volume
if "call_center" in df.columns:
    cc_counts = df["call_center"].astype(str).value_counts(dropna=True)
    cc_counts.to_csv(f"{OUT_DIR}/call_center_counts.csv", header=["count"])
 
# Duration stats
if "call_duration_in_minutes" in df.columns:
    dur = pd.to_numeric(df["call_duration_in_minutes"], errors="coerce")
    insights["avg_call_duration_min"] = round(float(dur.mean()), 3) if dur.notna().any() else None
    insights["p95_call_duration_min"] = round(float(dur.quantile(0.95)), 3) if dur.notna().any() else None
 
# Response time (if numeric-ish)
if "response_time" in df.columns:
    insights["avg_response_time"] = safe_mean(df["response_time"])
 
# State-wise CSAT (if available)
if "state" in df.columns and "csat_score" in df.columns:
    tmp = df[["state", "csat_score"]].copy()
    tmp["csat_score"] = pd.to_numeric(tmp["csat_score"], errors="coerce")
    state_csat = (
        tmp.dropna(subset=["state"])
           .groupby("state")["csat_score"]
           .mean()
           .sort_values()
    )
    state_csat.head(10).to_csv(f"{OUT_DIR}/lowest_state_csat.csv", header=["avg_csat"])
    state_csat.tail(10).sort_values(ascending=False).to_csv(f"{OUT_DIR}/highest_state_csat.csv", header=["avg_csat"])
 
# Save insights summary
pd.Series(insights).to_csv(f"{OUT_DIR}/insights_summary.csv", header=["value"])
 
print("=== ANALYSIS DONE ===")
print("Saved reports/ -> insights_summary.csv + breakdown CSVs (sentiment, reasons, channel, call_center, state csat)")
 