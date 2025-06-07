# app.py

import streamlit as st
from logic import unilateral_plan, bilateral_plan

st.set_page_config(page_title="Strabismus Surgical Planner", layout="centered")
st.title("Strabismus Surgical Planning App")

st.sidebar.header("Input Parameters")
deviation_type = st.sidebar.selectbox("Deviation Type", ["exotropia", "esotropia", "hypertropia", "hypotropia"])
deviation_pd = st.sidebar.number_input("Deviation Amount (in PD)", min_value=1, max_value=100, value=40)

st.sidebar.markdown("---")
approach = st.sidebar.radio("Select Surgical Approach", ["Unilateral", "Bilateral"])

st.markdown(f"### Surgical Plan for {deviation_pd} PD {deviation_type.title()}")

if approach == "Unilateral":
    plan = unilateral_plan(deviation_type, deviation_pd)
    if plan.get("status") == "Not allowed":
        st.error("Unilateral approach not possible: " + plan["reason"])
    else:
        st.success("Unilateral approach allowed")
        for key, value in plan.items():
            if key != "status":
                st.write(f"**{key}**: {value} mm")
else:
    plan = bilateral_plan(deviation_type, deviation_pd)
    st.success("Bilateral approach plan:")
    for key, value in plan.items():
        st.write(f"**{key}**: {value} mm")

st.markdown("---")
st.caption("Created for clinical planning of horizontal and vertical strabismus corrections.")
