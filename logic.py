
import pandas as pd

# Load the strabismus nomogram CSV
def load_nomogram(filepath="strabismus_nomogram.csv"):
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        raise FileNotFoundError("Nomogram CSV file not found. Please ensure 'strabismus_nomogram.csv' exists.")

def get_surgical_plan(strabismus_type, deviation_pd, approach, df=None):
    if df is None:
        df = load_nomogram()

    # Filter based on user input
    filtered = df[
        (df["Strabismus_Type"].str.lower() == strabismus_type.lower()) &
        (df["Deviation_PD"] == deviation_pd) &
        (df["Approach"].str.lower() == approach.lower())
    ]

    if filtered.empty:
        return "No surgical plan found for the selected parameters."

    # Format the output plan nicely
    result = []
    for _, row in filtered.iterrows():
        muscle = row["Muscle"]
        surgery_type = row["Surgery_Type"]
        recession = row["Recession_mm"]
        resection = row["Resection_mm"]

        if surgery_type.lower() == "recession" and not pd.isna(recession):
            result.append(f"• {muscle}: {surgery_type} of {recession:.1f} mm")
        elif surgery_type.lower() == "resection" and not pd.isna(resection):
            result.append(f"• {muscle}: {surgery_type} of {resection:.1f} mm")

    return "\n".join(result)
