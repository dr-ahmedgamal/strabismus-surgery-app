
import pandas as pd

def recommend_surgery(strabismus_type, deviation, approach, csv_file="strabismus_nomogram.csv"):
    df = pd.read_csv(csv_file)

    filtered = df[
        (df["Strabismus_Type"] == strabismus_type) &
        (df["Deviation_PD"] == deviation) &
        (df["Approach"] == approach)
    ]

    if filtered.empty:
        return "No recommendation found for the selected parameters."

    recommendations = {}
    for _, row in filtered.iterrows():
        muscle = row["Muscle"]
        surgery_type = row["Surgery_Type"]
        recession = row["Recession_mm"]
        resection = row["Resection_mm"]

        if muscle not in recommendations:
            recommendations[muscle] = {}

        if recession > 0:
            recommendations[muscle]["Recession"] = recession
        if resection > 0:
            recommendations[muscle]["Resection"] = resection

    return recommendations
