
import streamlit as st
import pandas as pd

# Load the CSV file
df = pd.read_csv("strabismus_nomogram.csv")

st.set_page_config(page_title="Strabismus Surgery Nomogram", layout="centered")

st.title("👁️ Strabismus Surgery Nomogram Helper")

# User inputs
strabismus_type = st.selectbox("Select Strabismus Type", df["Strabismus_Type"].unique())
deviation = st.selectbox("Enter Deviation (in Prism Diopters)", sorted(df["Deviation_PD"].unique()))
approach = st.selectbox("Select Approach", df["Approach"].unique())

# Filter based on input
filtered = df[
    (df["Strabismus_Type"] == strabismus_type) &
    (df["Deviation_PD"] == deviation) &
    (df["Approach"] == approach)
]

st.subheader("Recommended Muscle Surgeries")
st.dataframe(filtered.reset_index(drop=True))

st.markdown("---")
st.caption("This tool is based on customizable surgical nomograms. Always confirm with clinical judgment.")
