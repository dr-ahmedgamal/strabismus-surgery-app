import streamlit as st
from logic import plan_unilateral, plan_bilateral, unilateral_feasible

st.title("Strabismus Surgery Planning")

deviation_type = st.selectbox(
    "Select deviation type:",
    ["Exotropia", "Esotropia", "Hypertropia", "Hypotropia"],
)

amount_pd = st.number_input(
    "Enter deviation amount (in PD):", min_value=1, step=5, value=20
)

approach = st.radio("Select surgical approach:", ["Unilateral", "Bilateral"])

if st.button("Calculate plan"):
    if approach == "Unilateral":
        if unilateral_feasible(deviation_type, amount_pd):
            result = plan_unilateral(deviation_type, amount_pd)
            st.subheader("Unilateral Surgical Plan")
            for k, v in result.items():
                st.write(f"{k}: {v} mm")
        else:
            st.warning(
                "Unilateral approach is NOT feasible for this deviation.\n"
                "Switching to Bilateral approach automatically."
            )
            result = plan_bilateral(deviation_type, amount_pd)
            st.subheader("Bilateral Surgical Plan")
            for k, v in result.items():
                st.write(f"{k}: {v} mm")

    else:  # Bilateral approach
        result = plan_bilateral(deviation_type, amount_pd)
        st.subheader("Bilateral Surgical Plan")
        for k, v in result.items():
            st.write(f"{k}: {v} mm")
