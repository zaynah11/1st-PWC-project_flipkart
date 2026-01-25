import pandas as pd
 
def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
 
    # Standardize column names
    df.columns = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
 
    # Remove duplicate rows
    df = df.drop_duplicates()
 
    # Handle missing csat_score
    if "csat_score" in df.columns:
        df["csat_score"] = pd.to_numeric(df["csat_score"], errors="coerce")
        df["csat_score"] = df["csat_score"].fillna(df["csat_score"].median())
 
    # Convert call duration to numeric
    if "call_duration_in_minutes" in df.columns:
        df["call_duration_in_minutes"] = pd.to_numeric(
            df["call_duration_in_minutes"], errors="coerce"
        )
 
    return df