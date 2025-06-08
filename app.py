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
        feasible = unilateral_feasible(deviation_type, amount_pd)
        if feasible:
            plan = plan_unilateral(deviation_type, amount_pd)
            st.subheader("Unilateral Surgical Plan")
            for muscle, mm in plan.items():
                st.write(f"{muscle}: {mm} mm")
        else:
            st.warning(
                "Unilateral approach is NOT feasible for this deviation amount.\n"
                "Switching automatically to Bilateral approach."
            )
            plan = plan_bilateral(deviation_type, amount_pd)
            st.subheader("Bilateral Surgical Plan")
            for muscle, mm in plan.items():
                st.write(f"{muscle}: {mm} mm")

    else:  # Bilateral approach selected
        plan = plan_bilateral(deviation_type, amount_pd)
        st.subheader("Bilateral Surgical Plan")
        for muscle, mm in plan.items():
            st.write(f"{muscle}: {mm} mm")
