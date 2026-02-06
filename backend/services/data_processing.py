import pandas as pd


def process_csv(file_path: str):
    df = pd.read_csv(file_path)

    return {
        "revenue": float(df["revenue"].sum()),
        "expenses": float(df["expenses"].sum()),
        "debt": float(df.get("debt", pd.Series([0])).sum()),
        "cash": float(df.get("cash", pd.Series([0])).sum()),
    }