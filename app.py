import streamlit as st
import pandas as pd
from logic import get_recommendation

# Load the nomogram data
nomogram_file = "strabismus_nomogram.csv"
df = pd.read_csv(nomogram_file)

st.title("Strabismus Surgery Planner")
st.markdown("### Select Deviation Type and Amount")

# Strabismus type dropdown
strabismus_type = st.selectbox("Deviation Type", sorted(df["Strabismus_Type"].unique()))

# Deviation values dropdown based on type
available_deviations = sorted(df[df["Strabismus_Type"] == strabismus_type]["Deviation_PD"].unique())
deviation = st.selectbox("Deviation (Prism Diopters)", available_deviations)

# Approach dropdown
approach = st.selectbox("Surgical Approach", ["Unilateral", "Bilateral"])

# Submit button
if st.button("Show Recommendation"):
    recommendations = get_recommendation(strabismus_type, deviation, approach)

    st.markdown("## 🏥 Surgical Recommendation:")
    if recommendations:
        for line in recommendations:
            st.markdown(f"<div style='font-size:18px; padding:4px;'>🔹 {line}</div>", unsafe_allow_html=True)
    else:
        st.warning("No recommendation found for the selected parameters.")
