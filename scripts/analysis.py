import sys, os
import numpy as np
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
 
import pandas as pd
from db_connection import engine
 
TABLE_NAME = "final_table"
OUT_DIR = "reports-5"
os.makedirs(OUT_DIR, exist_ok=True)
 
# Load limited data for speed
df = pd.read_sql(f'SELECT * FROM "{TABLE_NAME}" LIMIT 50000', engine)
 
# -----------------------
# Safe numeric conversion
# -----------------------
if "csat_score" in df.columns:
    df["csat_score"] = pd.to_numeric(df["csat_score"], errors="coerce")
if "call_duration_in_minutes" in df.columns:
    df["call_duration_in_minutes"] = pd.to_numeric(df["call_duration_in_minutes"], errors="coerce")
if "response_time" in df.columns:
    df["response_time"] = pd.to_numeric(df["response_time"], errors="coerce")
 
# =====================================================
# TABLE 1: KPI SUMMARY
# =====================================================
summary_rows = [("total_rows_loaded", int(len(df))), ("total_columns", int(len(df.columns)))]
 
if "csat_score" in df.columns:
    csat = df["csat_score"]
    summary_rows += [
        ("avg_csat", round(float(csat.mean()), 3) if csat.notna().any() else None),
        ("median_csat", round(float(csat.median()), 3) if csat.notna().any() else None),
    ]
 
if "call_duration_in_minutes" in df.columns:
    dur = df["call_duration_in_minutes"]
    summary_rows += [
        ("avg_call_duration_min", round(float(dur.mean()), 3) if dur.notna().any() else None),
        ("p95_call_duration_min", round(float(dur.quantile(0.95)), 3) if dur.notna().any() else None),
    ]
 
if "response_time" in df.columns:
    rt = df["response_time"]
    summary_rows += [("avg_response_time", round(float(rt.mean()), 3) if rt.notna().any() else None)]
 
summary_df = pd.DataFrame(summary_rows, columns=["metric", "value"])
 
# =====================================================
# TABLE 2: TOP REASONS
# =====================================================
if "reason" in df.columns:
    top_reasons_df = (
        df["reason"].astype(str).replace("nan", pd.NA).dropna()
        .value_counts().head(15).reset_index()
    )
    top_reasons_df.columns = ["reason", "count"]
else:
    top_reasons_df = pd.DataFrame(columns=["reason", "count"])
 
# =====================================================
# TABLE 3: SENTIMENT DISTRIBUTION
# =====================================================
if "sentiment" in df.columns:
    sentiment_df = (
        df["sentiment"].astype(str).replace("nan", pd.NA).dropna()
        .value_counts().head(10).reset_index()
    )
    sentiment_df.columns = ["sentiment", "count"]
else:
    sentiment_df = pd.DataFrame(columns=["sentiment", "count"])
 
# =====================================================
# TABLE 4: CSAT BY STATE
# =====================================================
if {"state", "csat_score"}.issubset(df.columns):
    csat_by_state_df = (
        df.dropna(subset=["state"])
          .groupby("state", as_index=False)
          .agg(
              avg_csat=("csat_score", "mean"),
              tickets=("csat_score", "count")
          )
          .sort_values("avg_csat")
    )
    csat_by_state_df["avg_csat"] = csat_by_state_df["avg_csat"].round(3)
else:
    csat_by_state_df = pd.DataFrame(columns=["state", "avg_csat", "tickets"])


# def weighted_avg_csat(group_df, value, weight):
#     val = group_df[value]
#     wt = group_df[weight]
#     return (val*wt).sum() / wt.sum()
# =====================================================
# TABLE 5: CSAT BY STATE + CHANNEL + SENTIMENT
# =====================================================
needed = {"state", "channel", "sentiment", "csat_score"}
if needed.issubset(df.columns):
    csat_state_channel_sentiment_df = (
        df.dropna(subset=["state", "channel", "sentiment"])
          .groupby(["state", "channel", "sentiment"], as_index=False)
          .agg(
              avg_csat=("csat_score", "mean"),
              tickets=("csat_score", "count")
          )
          .sort_values("tickets", ascending=False)
    )
    csat_state_channel_sentiment_df["avg_csat"] = csat_state_channel_sentiment_df["avg_csat"].round(3)
    # channels_grouped = csat_state_channel_sentiment_df.groupby(['channel', 'sentiment']).apply(weighted_avg_csat, 'avg_csat', 'tickets')
else:
    csat_state_channel_sentiment_df = pd.DataFrame(
        columns=["state", "channel", "sentiment", "avg_csat", "tickets"]
    )
 

# =====================================================
# TABLE 6: CHANNEL + CALL CENTER + CSAT   (NEW)
# =====================================================
needed2 = {"channel", "call_center", "csat_score"}
if needed2.issubset(df.columns):
    channel_callcenter_csat_df = (
        df.dropna(subset=["channel", "call_center"])
          .groupby(["channel", "call_center"], as_index=False)
          .agg(
              avg_csat=("csat_score", "mean"),
              tickets=("csat_score", "count")
          )
          .sort_values("tickets", ascending=False)
    )
    channel_callcenter_csat_df["avg_csat"] = channel_callcenter_csat_df["avg_csat"].round(3)
else:
    channel_callcenter_csat_df = pd.DataFrame(
        columns=["channel", "call_center", "avg_csat", "tickets"]
    )
 
# =====================================================
# SAVE ALL TABLES
# =====================================================
summary_df.to_csv(f"{OUT_DIR}/1_kpi_summary.csv", index=False)
top_reasons_df.to_csv(f"{OUT_DIR}/2_top_reasons.csv", index=False)
sentiment_df.to_csv(f"{OUT_DIR}/3_sentiment.csv", index=False)
csat_by_state_df.to_csv(f"{OUT_DIR}/4_csat_by_state.csv", index=False)
csat_state_channel_sentiment_df.to_csv(f"{OUT_DIR}/5_csat_state_channel_sentiment.csv", index=False)
channel_callcenter_csat_df.to_csv(f"{OUT_DIR}/6_channel_callcenter_csat.csv", index=False)
# channels_grouped.to_csv(f"{OUT_DIR}/6_channel_callcenter_csat_weighted_avg.csv", index=False)
print("=== DONE SUCCESSFULLY ===")
print("CSV tables saved in:", OUT_DIR)
print("6_channel_callcenter_csat.csv added")
 