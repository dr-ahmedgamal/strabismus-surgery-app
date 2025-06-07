import streamlit as st
from logic import calculate_surgery

st.set_page_config(page_title="Strabismus Surgical Planner", layout="centered")

st.title("Strabismus Surgical Planning Tool")
st.markdown("""
#### Fill out the form below, then click **Show Recommendation** to generate a tailored surgical plan based on the type and magnitude of deviation.
""")

# Sidebar form with button to trigger processing
with st.form(key="surgery_form"):
    deviation_type = st.selectbox("Deviation Type", ["Esotropia", "Exotropia", "Hypertropia", "Hypotropia"])

    if deviation_type in ["Esotropia", "Exotropia"]:
        deviation_range = list(range(15, 85, 5))
    else:
        deviation_range = list(range(5, 50, 5))

    deviation_value = st.selectbox("Deviation in Prism Diopters", deviation_range)
    approach = st.selectbox("Surgical Approach", ["Unilateral", "Bilateral"])

    submitted = st.form_submit_button("Show Recommendation")

if submitted:
    results = calculate_surgery(deviation_type, deviation_value, approach)

    st.markdown("---")
    st.subheader("Recommended Surgical Plan")

    if results:
        for step in results:
            st.markdown(f"<div style='font-size:18px; padding:6px;'>{step}</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size:18px; color:red;'>No surgical correction recommended.</div>", unsafe_allow_html=True)
