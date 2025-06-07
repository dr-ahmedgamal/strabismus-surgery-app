# app.py
import streamlit as st
from logic import calculate_plan

st.title("Strabismus Surgical Planning App")

deviation_type = st.selectbox(
    "Select deviation type",
    ['esotropia', 'exotropia', 'hypertropia', 'hypotropia']
)

deviation_pd = st.slider("Deviation amount (PD)", 15, 90, 30)

approach = st.radio(
    "Select surgical approach",
    ['unilateral', 'bilateral']
)

if st.button("Calculate Plan"):
    plan = calculate_plan(deviation_pd, deviation_type, approach)
    
    st.subheader("Surgical Plan")
    for muscle, mm in plan.items():
        st.write(f"{muscle}: {mm} mm")
