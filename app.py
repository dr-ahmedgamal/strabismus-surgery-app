import streamlit as st
from logic import calculate_surgery

st.set_page_config(page_title="Strabismus Surgical Planner", layout="centered")

st.title("Strabismus Surgical Planner")
st.markdown("""
Use the dropdown menus below to choose deviation type, deviation amount, and surgical approach.
Click **Show Recommendation** to see a personalized surgical plan.
""")

# User input controls
deviation_type = st.selectbox("Select Deviation Type", ["Esotropia", "Exotropia", "Hypertropia", "Hypotropia"])
deviation_value = st.selectbox("Select Deviation (in Prism Diopters)", list(range(15, 95, 5)))
approach = st.selectbox("Surgical Approach", ["Unilateral", "Bilateral"])

# Button to trigger recommendation
if st.button("Show Recommendation"):
    try:
        recommendations = calculate_surgery(deviation_type, deviation_value, approach)

        if recommendations:
            st.markdown("### Recommended Surgical Plan:")
            for rec in recommendations:
                st.markdown(f"<div style='font-size:20px; padding:6px 0;'>{rec}</div>", unsafe_allow_html=True)
        else:
            st.warning("No recommendation found for selected options.")
    except Exception as e:
        st.error(f"An error occurred while calculating recommendation: {e}")
