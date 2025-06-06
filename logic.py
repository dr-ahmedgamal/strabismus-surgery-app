
import pandas as pd

def load_nomogram(file_path="strabismus_nomogram.csv"):
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        raise FileNotFoundError(f"Could not load the CSV file: {e}")

def get_surgery_plan(df, strabismus_type, deviation_pd, approach):
    filtered = df[
        (df["Strabismus_Type"] == strabismus_type) &
        (df["Deviation_PD"] == deviation_pd) &
        (df["Approach"] == approach)
    ]
    if filtered.empty:
        return None
    return filtered
