import streamlit as st
from logic import calculate_surgery

st.set_page_config(page_title="Strabismus Surgery Planner", layout="centered")

st.title("Strabismus Surgery Recommendation App")

# Dropdown for deviation type
deviation_type = st.selectbox(
    "Select Deviation Type",
    ["Esotropia", "Exotropia", "Hypertropia", "Hypotropia"]
)

# Numeric input for deviation value with start=15 and step=5
deviation_value = st.number_input(
    "Enter Deviation Value (Prism Diopters)",
    min_value=1, max_value=150, step=5,
    value=15,
    format="%d"
)

# Dropdown for surgical approach
approach = st.selectbox(
    "Select Surgical Approach",
    ["Unilateral", "Bilateral"]
)

# Show results on button click only
if st.button("Show Recommendation"):
    if deviation_value <= 0:
        st.warning("Please enter a deviation value greater than zero.")
    else:
        plan = calculate_surgery(deviation_type, deviation_value, approach)
        if plan:
            st.subheader("Recommended Surgery Plan:")

            # Separate corrections by eye
            affected_eye_procedures = []
            other_eye_procedures = []

            for proc in plan:
                if proc.startswith("Affected Eye"):
                    affected_eye_procedures.append(proc.replace("Affected Eye ", ""))
                elif proc.startswith("Other Eye"):
                    other_eye_procedures.append(proc.replace("Other Eye ", ""))
                else:
                    # Fallback: put it in affected eye if unclear
                    affected_eye_procedures.append(proc)

            # Display affected eye corrections first
            if affected_eye_procedures:
                st.markdown("**Affected Eye Corrections:**")
                for i, proc in enumerate(affected_eye_procedures, 1):
                    st.markdown(f"{i}. {proc}")

            # Display other eye corrections next
            if other_eye_procedures:
                st.markdown("**Other Eye Corrections:**")
                for i, proc in enumerate(other_eye_procedures, 1):
                    st.markdown(f"{i}. {proc}")

        else:
            st.info("No surgical plan generated for given inputs.")
