import streamlit as st
from logic import plan_unilateral

st.title("Strabismus Surgery Planning Tool")

deviation_type = st.selectbox("Select deviation type:", ["Exotropia", "Esotropia", "Hypertropia", "Hypotropia"])

# Use number_input instead of selectbox for PD
amount_pd = st.number_input("Deviation amount (PD):", min_value=15, max_value=100, step=5, value=15)

approach = st.radio("Preferred approach:", ["Unilateral", "Bilateral"])

if st.button("Calculate Surgical Plan"):
    plan = None
    switched = False

    if approach == "Unilateral":
        plan = plan_unilateral(deviation_type, amount_pd)
        if plan["approach"] == "Bilateral":
            switched = True
    else:
        from logic import plan_bilateral
        plan = plan_bilateral(deviation_type, amount_pd)

    if switched:
        st.warning("⚠️ Unilateral correction not sufficient — switched to bilateral plan.")

    st.subheader(f"{plan['approach']} Surgical Plan")
    for key, value in plan.items():
        if key != "approach":
            st.write(f"- **{key}**: {value} mm")
