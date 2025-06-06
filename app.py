import streamlit as st
import pandas as pd

st.set_page_config(page_title="Strabismus Surgical Planner", layout="centered")
st.title("👁️ Strabismus Surgical Planner")

# Load the CSV file
df = pd.read_csv("strabismus_nomogram_full.csv")

# User Inputs
strabismus_type = st.selectbox("Strabismus Type", df["Type"].unique())
laterality = st.selectbox("Approach", ["Unilateral", "Bilateral"])
angle = st.slider("Deviation (prism diopters)", 15, 90, 30, step=5)

# Filter the dataset
results = df[
    (df["Type"] == strabismus_type) &
    (df["Laterality"] == laterality) &
    (df["Angle"] == angle)
]

if results.empty:
    st.warning("No surgical plan found for this configuration.")
else:
    st.markdown("### Suggested Surgical Plan")
    st.dataframe(results[["Muscle(s)", "Recession_mm", "Resection_mm"]])