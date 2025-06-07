import streamlit as st
from logic import unilateral_approach, bilateral_approach

st.title("Strabismus Surgery Planning")

st.markdown(
    """
    This app calculates recommended recession and resection muscle lengths for strabismus correction.
    Choose deviation type, approach, and enter deviation angle (in PD).
    """
)

# Select deviation type
deviation_type = st.selectbox(
    "Select Deviation Type:",
    options=["Esotropia", "Exotropia", "Hypertropia", "Hypotropia"]
).lower()

# Select surgical approach
approach = st.selectbox(
    "Select Surgical Approach:",
    options=["Unilateral", "Bilateral"]
).lower()

# Deviation input with step 5
pd_value = st.number_input(
    "Enter Deviation Angle (PD):",
    min_value=15,
    max_value=100,
    step=5,
    value=30,
    format="%d"
)

# Button to calculate
if st.button("Calculate Surgery Plan"):
    try:
        if approach == "unilateral":
            result = unilateral_approach(deviation_type, pd_value)
        else:
            result = bilateral_approach(deviation_type, pd_value)

        if "error" in result:
            st.error(result["error"])
        else:
            st.success("Recommended Surgical Plan:")
            for muscle_action, length in result.items():
                if length == "Not needed":
                    st.info(f"{muscle_action.replace('_', ' ').title()}: {length}")
                else:
                    st.write(f"**{muscle_action.replace('_', ' ').title()}**: {length} mm")

    except Exception as e:
        st.error(f"Error: {str(e)}")
