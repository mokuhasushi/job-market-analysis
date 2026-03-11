import pandas as pd

def clean_data(df: pd.DataFrame):

    df = df.drop_duplicates()

    df["Job Title"] = df["Job Title"].str.strip()

    df["Company"] = df["Company"].fillna("Unknown")

    df["Location"] = df["Location"].fillna("Unknown")

    return df