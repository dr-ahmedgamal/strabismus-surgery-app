import streamlit as st
from logic import calculate_surgery

st.set_page_config(page_title="Strabismus Surgical Planner")

st.title("Strabismus Surgical Planner")
st.markdown("### Enter deviation details:")

deviation_type = st.selectbox("Deviation Type", ["Esotropia", "Exotropia", "Hypertropia", "Hypotropia"])
deviation_value = st.number_input("Deviation (in Prism Diopters)", min_value=15, step=5, value=15)
approach = st.radio("Surgical Approach", ["Unilateral", "Bilateral"])

if st.button("Get Surgical Plan"):
    result = calculate_surgery(deviation_type, deviation_value, approach)
    st.subheader("Surgical Recommendation")
    if result["Affected Eye"]:
        st.markdown("**Affected Eye Correction:** " + ", ".join(result["Affected Eye"]))
    if result["Other Eye"]:
        st.markdown("**Other Eye Correction:** " + ", ".join(result["Other Eye"]))
