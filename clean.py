import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # ---- Standardize column names ----
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[ -]+", "_", regex=True)
    )

    # ---- Drop fully empty rows & columns ----
    df = df.dropna(axis=0, how="all")
    df = df.dropna(axis=1, how="all")

    # ---- Remove duplicates ----
    df = df.drop_duplicates()

    # ---- Normalize text columns ----
    for col in df.select_dtypes(include="object").columns:
        df[col] = (
            df[col]
            .astype(str)
            .str.strip()
            .str.lower()
            .replace(
                ["", "none", "null", "nan", "na", "n/a", "undefined"],
                pd.NA
            )
        )

    # ---- Force numeric conversion where possible ----
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # ---- Fill numeric nulls ----
    num_cols = df.select_dtypes(include="number").columns
    for col in num_cols:
        if df[col].notna().any():
            df[col] = df[col].fillna(df[col].median())
        else:
            # all values are null → fill with 0 (or drop column)
            df[col] = df[col].fillna(0)

    return df
