import streamlit as st
from logic import calculate_surgery

st.set_page_config(page_title="Strabismus Surgery Planner", layout="centered")

st.title("Strabismus Surgery Recommendation App")

deviation_type = st.selectbox(
    "Select Deviation Type",
    ["Esotropia", "Exotropia", "Hypertropia", "Hypotropia"]
)

deviation_value = st.number_input(
    "Enter Deviation Value (Prism Diopters)",
    min_value=1, max_value=150, step=1
)

approach = st.selectbox(
    "Select Surgical Approach",
    ["Unilateral", "Bilateral"]
)

if st.button("Show Recommendation"):
    if deviation_value <= 0:
        st.warning("Please enter a deviation value greater than zero.")
    else:
        plan = calculate_surgery(deviation_type, deviation_value, approach)
        if plan:
            st.subheader("Recommended Surgery Plan:")
            for procedure in plan:
                st.markdown(f"- **{procedure}**")
        else:
            st.info("No surgical plan generated for given inputs.")
