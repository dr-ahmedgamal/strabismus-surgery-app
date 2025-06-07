
import streamlit as st
import pandas as pd
from logic import recommend_surgery

st.set_page_config(page_title="Strabismus Surgery Planner", layout="centered")
st.title("Strabismus Surgical Planner")

df = pd.read_csv("strabismus_nomogram.csv")

st.markdown("### Please fill the following details to get surgical recommendation")

strabismus_types = df["Strabismus_Type"].unique()
selected_type = st.selectbox("Select Type of Strabismus", strabismus_types)

deviation_values = sorted(df[df["Strabismus_Type"] == selected_type]["Deviation_PD"].unique())
selected_deviation = st.selectbox("Select Deviation (Prism Diopters)", deviation_values)

approach = st.radio("Select Surgical Approach", options=["Unilateral", "Bilateral"])

if st.button("Show Recommendation"):
    result = recommend_surgery(selected_type, selected_deviation, approach)

    if isinstance(result, dict):
        st.subheader("Surgical Plan Recommendation:")
        for muscle, actions in result.items():
            parts = []
            if "Recession" in actions:
                parts.append(f"Recession: **{actions['Recession']} mm**")
            if "Resection" in actions:
                parts.append(f"Resection: **{actions['Resection']} mm**")
            if parts:
                st.markdown(f"- **{muscle}**: " + ", ".join(parts), unsafe_allow_html=True)
    else:
        st.warning(result)
