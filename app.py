import streamlit as st
import pandas as pd
from logic import calculate_correction_amounts

st.title("Strabismus Surgical Nomogram Calculator")

# Load CSV file with cases if needed (optional)
# data = pd.read_csv('strabismus_cases.csv')

deviation_types = ["Esotropia", "Exotropia", "Hypertropia", "Hypotropia"]
approaches = ["Unilateral", "Bilateral"]

# User input widgets
deviation_type = st.selectbox("Select deviation type:", deviation_types)
deviation_pd = st.slider("Enter deviation amount (Prism Diopters):", min_value=15, max_value=80, step=5)
approach = st.selectbox("Select surgical approach:", approaches)

if st.button("Calculate Surgical Plan"):
    try:
        corrections = calculate_correction_amounts(deviation_type, deviation_pd, approach)

        st.subheader("Surgical Recommendation")

        # Format affected eye corrections
        affected_corrs = corrections.get("affected_eye", [])
        affected_str = ", ".join([f"{muscle} of {amount} mm" for muscle, amount in affected_corrs])
        if affected_str:
            st.markdown(f"**Affected Eye Correction:** {affected_str}")

        # Format other eye corrections
        other_corrs = corrections.get("other_eye", [])
        other_str = ", ".join([f"{muscle} of {amount} mm" for muscle, amount in other_corrs])
        if other_str:
            st.markdown(f"**Other Eye Correction:** {other_str}")

        if not affected_str and not other_str:
            st.write("No corrections required for the given input.")

    except Exception as e:
        st.error(f"Error: {e}")
