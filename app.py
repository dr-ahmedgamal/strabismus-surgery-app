import streamlit as st
from logic import calculate_surgery

st.set_page_config(page_title="Strabismus Surgery Planner", layout="centered")

st.title("Strabismus Surgery Recommendation App")

# Dropdown for deviation type
deviation_type = st.selectbox(
    "Select Deviation Type",
    ["Esotropia", "Exotropia", "Hypertropia", "Hypotropia"]
)

# Numeric input for deviation value
deviation_value = st.number_input(
    "Enter Deviation Value (Prism Diopters)",
    min_value=1, max_value=150, step=1,
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
            # Display in a neat numbered list
            for i, procedure in enumerate(plan, 1):
                st.markdown(f"{i}. **{procedure}**")
        else:
            st.info("No surgical plan generated for given inputs.")
