import streamlit as st
from logic import calculate_surgery

st.set_page_config(page_title="Strabismus Surgery Planner", layout="centered")

st.title("Strabismus Surgery Recommendation App")

# Deviation type dropdown
deviation_type = st.selectbox(
    "Select Deviation Type",
    ["Esotropia", "Exotropia", "Hypertropia", "Hypotropia"]
)

# Deviation value input with min=15 and step=5
deviation_value = st.number_input(
    "Enter Deviation Value (Prism Diopters)",
    min_value=1, max_value=150, step=5,
    value=15,
    format="%d"
)

# Surgical approach dropdown
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

            affected_eye_procedures = []
            other_eye_procedures = []

            for proc in plan:
                if proc.startswith("Affected Eye"):
                    affected_eye_procedures.append(proc.replace("Affected Eye ", ""))
                elif proc.startswith("Other Eye"):
                    other_eye_procedures.append(proc.replace("Other Eye ", ""))
                else:
                    affected_eye_procedures.append(proc)

            if affected_eye_procedures:
                affected_text = ", ".join(affected_eye_procedures)
                st.markdown(f"**Affected Eye Correction:** {affected_text}")

            if other_eye_procedures:
                other_text = ", ".join(other_eye_procedures)
                st.markdown(f"**Other Eye Correction:** {other_text}")

        else:
            st.info("No surgical plan generated for given inputs.")
