import pandas as pd
import numpy as np
from datetime import datetime


# NULL FIX
def fix_nulls(df):
    null_like = ["", " ", "nan", "NaN", "NULL", "null", "None", "-", "undefined"]
    return df.replace(null_like, np.nan)


# WHITESPACE
def clean_whitespace(df):
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].astype(str).str.strip().str.replace(r"\s+", " ", regex=True)
        df[col] = df[col].replace("nan", np.nan)
    return df


# NUMERIC DETECTION
def detect_numeric(df):
    for col in df.columns:
        if df[col].dtype == "object":
            converted = pd.to_numeric(df[col], errors="coerce")
            if converted.notna().sum() > len(df)*0.6:
                df[col] = converted
    return df


# DATE DETECTION
def detect_dates(df):
    for col in df.columns:
        if df[col].dtype == "object":
            converted = pd.to_datetime(df[col], errors="coerce", format="mixed")
            if converted.notna().sum() > len(df)*0.7:
                df[col] = converted
    return df


# INVALID DATE FIX
def fix_invalid_dates(df):

    current_year = datetime.now().year

    for col in df.select_dtypes(include="datetime"):

        df.loc[df[col].dt.year < 1900, col] = np.nan
        df.loc[df[col].dt.year > current_year, col] = np.nan
        df.loc[df[col].dt.year == 1970, col] = np.nan

    return df


# NEGATIVE VALUES
def fix_negative(df):
    for col in df.select_dtypes(include="number"):
        df.loc[df[col] < 0, col] = np.nan
    return df


# TEXT NORMALIZE
def normalize_text(df):
    for col in df.select_dtypes(include="object"):
        df[col] = df[col].str.title()
    return df


# HANDLE MISSING
def handle_missing(df):

    for col in df.select_dtypes(include="number"):
        df[col] = df[col].fillna(df[col].median())

    for col in df.select_dtypes(include="object"):
        if not df[col].mode().empty:
            df[col] = df[col].fillna(df[col].mode()[0])

    for col in df.select_dtypes(include="datetime"):
        df[col] = df[col].fillna(df[col].median())

    return df


# OUTLIERS
def handle_outliers(df):

    for col in df.select_dtypes(include="number"):

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)

        iqr = q3 - q1

        lower = q1 - 1.5*iqr
        upper = q3 + 1.5*iqr

        df[col] = df[col].clip(lower, upper)

    return df


def finalize_types(df):

    for col in df.columns:

        # skip datetime
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            continue

        # try numeric conversion
        numeric = pd.to_numeric(df[col], errors="coerce")

        if numeric.notna().sum() > len(df) * 0.6:

            # integer detection
            if (numeric.dropna() % 1 == 0).all():
                df[col] = numeric.astype("Int64")
            else:
                df[col] = numeric.astype("float64")

            continue

        # try datetime conversion
        date = pd.to_datetime(df[col], errors="coerce", format="mixed")

        if date.notna().sum() > len(df) * 0.8:
            df[col] = date

    return df


# FULL PIPELINE
def full_clean_pipeline(df):

    df = fix_nulls(df)

    df = clean_whitespace(df)

    df = detect_numeric(df)

    df = detect_dates(df)

    df = fix_invalid_dates(df)

    df = fix_negative(df)

    df = normalize_text(df)

    df = handle_missing(df)

    df = handle_outliers(df)

    df = finalize_types(df)

    df = df.drop_duplicates().reset_index(drop=True)

    return df


# CLEANING REPORT
def generate_report(before, after):

    return pd.DataFrame({

        "Metric": ["Missing Values", "Duplicate Rows", "Rows"],

        "Before": [
            before.isnull().sum().sum(),
            before.duplicated().sum(),
            before.shape[0]
        ],

        "After": [
            after.isnull().sum().sum(),
            after.duplicated().sum(),
            after.shape[0]
        ]

    })


# DATATYPE TABLE
def get_datatype_table(df):

    return pd.DataFrame({
        "Column": df.columns,
        "Datatype": df.dtypes.astype(str)
    })