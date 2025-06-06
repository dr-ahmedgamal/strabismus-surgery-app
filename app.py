
import streamlit as st
import pandas as pd
from logic import get_surgical_plan, load_nomogram

st.set_page_config(page_title="Strabismus Surgical Planner", layout="centered")

# Load nomogram CSV
df = load_nomogram("strabismus_nomogram.csv")

st.title("👁️ Strabismus Surgical Planner")
st.markdown("Use this app to plan muscle surgeries based on deviation and type of strabismus.")

# User selections
strabismus_type = st.selectbox("Select Strabismus Type", sorted(df["Strabismus_Type"].unique()))
deviation_pd = st.selectbox("Select Deviation (Prism Diopters)", sorted(df["Deviation_PD"].unique()))
approach = st.radio("Select Surgical Approach", sorted(df["Approach"].unique()))

# Predict and show plan
if st.button("Get Surgical Plan"):
    result = get_surgical_plan(strabismus_type, deviation_pd, approach, df)
    st.subheader("Recommended Surgical Plan")
    st.code(result, language="markdown")
