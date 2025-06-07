import streamlit as st
from logic import plan_unilateral, plan_bilateral

st.title("Strabismus Surgery Planning")

deviation_type = st.selectbox("Select Deviation Type:", ["Esotropia", "Exotropia", "Hypertropia", "Hypotropia"])
amount_pd = st.slider("Enter deviation in Prism Diopters (PD):", min_value=15, max_value=120, step=5)
approach = st.selectbox("Select Surgical Approach:", ["Unilateral", "Bilateral"])

if st.button("Calculate Plan"):
    if approach == "Unilateral":
        plan, converted = plan_unilateral(deviation_type, amount_pd)
        if converted:
            st.warning("Unilateral approach is NOT feasible for full correction. Automatically switched to Bilateral approach.")
            approach = "Bilateral"  # Update UI or logic to show the switch
        else:
            st.success("Unilateral approach plan:")
    else:
        plan = plan_bilateral(deviation_type, amount_pd)
        st.success("Bilateral approach plan:")

    for muscle, value in plan.items():
        st.write(f"- **{muscle}**: {value} mm")
