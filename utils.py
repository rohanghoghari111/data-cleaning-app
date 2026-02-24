import pandas as pd
import numpy as np
from datetime import datetime

# ===================== UNIVERSAL LOGICAL CLEANER =====================

def convert_dates(df):
    date_cols = ["order_date", "Order Date"]
    for c in date_cols:
        if c in df.columns:
            df[c] = pd.to_datetime(df[c], errors="coerce")
    return df

def fix_textual_nulls(df):
    null_like = [
        "", " ", "  ", "nan", "NaN", "NAN",
        "null", "NULL", "None", "none",
        "undefined", "Undefined", "-"
    ]
    return df.replace(null_like, np.nan)

def clean_whitespace(df):
    for c in df.select_dtypes(include="object"):
        df[c] = (
            df[c]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
            .replace("nan", np.nan)
        )
    return df

def standardize_data(df):
    for c in df.select_dtypes(include="object"):
        if c.lower() != "certificate":
            df[c] = (
                df[c]
                .fillna("")
                .astype(str)
                .str.strip()
                .str.title()
                .replace("", np.nan)
            )

    mappings = {
        "platform": {
            "Amazom Prime": "Amazon Prime",
            "Zee 5": "Zee5"
        },
        "country": {
            "Indai": "India",
            "India ": "India"
        }
    }

    for col, mapping in mappings.items():
        if col in df.columns:
            df[col] = df[col].replace(mapping)

    if "certificate" in df.columns:
        df["certificate"] = (
            df["certificate"]
            .astype(str)
            .str.upper()
            .str.strip()
        )
        allowed = {"U", "UA", "A"}
        df.loc[~df["certificate"].isin(allowed), "certificate"] = np.nan

    return df

def convert_and_validate_numeric(df):
    numeric_candidates = [
        "release_year", "duration_min", "imdb_rating",
        "budget_cr", "box_office_cr", "profit_cr"
    ]

    for c in numeric_candidates:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    current_year = datetime.now().year

    if "release_year" in df.columns:
        df.loc[
            (df["release_year"] < 1800) |
            (df["release_year"] > current_year + 1),
            "release_year"
        ] = np.nan

    if "imdb_rating" in df.columns:
        df.loc[
            (df["imdb_rating"] < 0) |
            (df["imdb_rating"] > 10),
            "imdb_rating"
        ] = np.nan

    if "duration_min" in df.columns:
        df.loc[df["duration_min"] <= 0, "duration_min"] = np.nan
        df["duration_min"] = df["duration_min"].fillna(df["duration_min"].median())

    if "budget_cr" in df.columns:
        df.loc[df["budget_cr"] < 0, "budget_cr"] = np.nan
        df["budget_cr"] = df["budget_cr"].fillna(df["budget_cr"].median())

    if "box_office_cr" in df.columns:
        df.loc[df["box_office_cr"] < 0, "box_office_cr"] = np.nan
        df["box_office_cr"] = df["box_office_cr"].fillna(df["box_office_cr"].median())

    return df

def enforce_logic(df):
    if {"budget_cr", "box_office_cr"}.issubset(df.columns):
        df["profit_cr"] = df["box_office_cr"] - df["budget_cr"]
    return df

def finalize_types(df):
    if "release_year" in df.columns:
        df["release_year"] = df["release_year"].round().astype("Int64")

    if "duration_min" in df.columns:
        df["duration_min"] = df["duration_min"].round().astype("Int64")

    if "imdb_rating" in df.columns:
        df["imdb_rating"] = df["imdb_rating"].round(1)

    return df

# ===================== FINAL PIPELINE =====================

def full_clean_pipeline(df):
    df = fix_textual_nulls(df)
    df = clean_whitespace(df)
    df = standardize_data(df)
    df = convert_and_validate_numeric(df)
    df = convert_dates(df)
    df = enforce_logic(df)
    df = df.drop_duplicates().reset_index(drop=True)
    df = finalize_types(df)
    return df

def get_datatype_table(df):
    return pd.DataFrame({
        "Column": df.columns,
        "Datatype": df.dtypes.astype(str)
    })

def generate_report(before, after):
    return pd.DataFrame([
        {
            "Metric": "Missing Values",
            "Before": int(before.isnull().sum().sum()),
            "After": int(after.isnull().sum().sum())
        },
        {
            "Metric": "Duplicate Rows",
            "Before": int(before.duplicated().sum()),
            "After": int(after.duplicated().sum())
        }
    ])







