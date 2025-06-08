import streamlit as st
from logic import plan_unilateral, plan_bilateral

st.title("Strabismus Surgery Planning")

deviation_types = ["Exotropia", "Esotropia", "Hypertropia", "Hypotropia"]
deviation = st.selectbox("Select Deviation Type:", deviation_types)

amount_pd = st.number_input("Enter Deviation in Prism Diopters (PD):", min_value=5, max_value=150, step=5)

approach = st.radio("Choose Surgical Approach:", ["Unilateral", "Bilateral"])

result = None
message = ""

if st.button("Calculate"):
    if approach == "Unilateral":
        result = plan_unilateral(deviation, amount_pd)
        if result is None:
            message = ("Unilateral approach is NOT feasible for full correction of this deviation. "
                       "Showing bilateral approach plan instead.")
            result = plan_bilateral(deviation, amount_pd)
    else:
        result = plan_bilateral(deviation, amount_pd)

    if result:
        st.subheader("Surgical Plan:")
        for muscle, value in result.items():
            st.write(f"{muscle}: {value} mm")
    else:
        st.warning("No surgical plan available for the given parameters.")

    if message:
        st.info(message)
