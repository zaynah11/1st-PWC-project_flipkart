import pandas as pd

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # -------------------------------------------------
    # Standardize column names
    # Example: "Customer Name" → "customer_name"
    # -------------------------------------------------
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[ -]+", "_", regex=True)
    )

    # -------------------------------------------------
    # Drop fully empty rows & columns
    # -------------------------------------------------
    df = df.dropna(axis=0, how="all")
    df = df.dropna(axis=1, how="all")

    # -------------------------------------------------
    # Remove duplicate rows
    # -------------------------------------------------
    df = df.drop_duplicates()

    # -------------------------------------------------
    # Normalize text (object) columns
    # - trim spaces
    # - lowercase
    # - convert fake nulls to real nulls
    # -------------------------------------------------
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

    # -------------------------------------------------
    # Force numeric conversion safely
    # Invalid numeric values → NaN (do NOT crash)
    # -------------------------------------------------
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # =================================================
    # ❌ REMOVED LOGIC (DO NOT USE FOR REPORTING)
    # This was IMPUTING (inventing) numeric values
    # which can distort analytics
    # =================================================
    """
    num_cols = df.select_dtypes(include="number").columns
    for col in num_cols:
        if df[col].notna().any():
            df[col] = df[col].fillna(df[col].median())
        else:
            df[col] = df[col].fillna(0)
    """

    # -------------------------------------------------
    # ✅ CORRECT LOGIC FOR ANALYTICS
    # Remove rows with missing numeric values
    # (Keeps data honest, no fake numbers)
    # -------------------------------------------------
    num_cols = df.select_dtypes(include="number").columns
    df = df.dropna(subset=num_cols)

    return df
