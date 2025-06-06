
import streamlit as st
from logic import StrabismusSurgeryRecommender

st.title("Strabismus Surgery Recession/Resection Recommender")

# Load recommender
recommender = StrabismusSurgeryRecommender("strabismus_nomogram_0.5step.csv")

# User inputs
strabismus_type = st.selectbox("Select Strabismus Type", ["Esotropia", "Exotropia"])
deviation = st.slider("Enter Deviation (Prism Diopters)", 15, 90, step=1)
approach = st.selectbox("Select Approach", ["Unilateral", "Bilateral"])

if st.button("Get Recommendation"):
    results = recommender.recommend(strabismus_type, deviation, approach)
    st.markdown("### Recommended Surgery Details:")
    for r in results:
        st.write(f"Muscle: {r['Muscle']}")
        st.write(f"  Surgery Type: {r['Surgery_Type']}")
        if r['Recession_mm']:
            st.write(f"  Recession (mm): {r['Recession_mm']}")
        if r['Resection_mm']:
            st.write(f"  Resection (mm): {r['Resection_mm']}")
        st.write("---")
