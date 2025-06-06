import streamlit as st
import pandas as pd
from logic import get_recommendation  # assuming your logic.py has this function

# Load CSV nomogram
df = pd.read_csv("strabismus_nomogram.csv")

st.title("Strabismus Surgery Planner")

# Sidebar info
st.sidebar.header("Input Parameters")

# Strabismus Type selection
strabismus_type = st.sidebar.selectbox("Strabismus Type", df["Strabismus_Type"].unique())

# Deviation selection - dropdown with steps of 5 from 15 to 90 (prism diopters)
deviation_range = list(range(15, 95, 5))
deviation = st.sidebar.selectbox("Deviation (prism diopters)", deviation_range)

# Approach selection
approach = st.sidebar.radio("Approach", ["Unilateral", "Bilateral"])

# Button to show recommendation
if st.sidebar.button("Show Recommendation"):
    result = get_recommendation(strabismus_type, deviation, approach, df)

    st.subheader("Surgical Recommendation")

    if not result:
        st.write("No valid recommendation found for the given inputs.")
    else:
        for eye, corrections in result.items():
            st.markdown(f"**{eye} eye corrections:**")
            for muscle, measures in corrections.items():
                lines = []
                if measures.get("Recession_mm", 0) > 0:
                    lines.append(f"Recession: {measures['Recession_mm']} mm")
                if measures.get("Resection_mm", 0) > 0:
                    lines.append(f"Resection: {measures['Resection_mm']} mm")
                if lines:
                    st.markdown(f"- {muscle}: " + ", ".join(lines))

    # Remove the footer lines as requested
    # st.write("Fill the form and click Show Recommendation to display results.")
    # st.write("Created to support precise ophthalmic strabismus surgical planning.")
