import streamlit as st
import pandas as pd
from logic import calculate_surgery

st.set_page_config(page_title="Strabismus Surgical Planner", layout="centered")
st.title("Strabismus Surgical Recommendation App")

st.markdown("Upload a CSV file or manually input the deviation details to get surgical recommendations.")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

def display_plan(plan):
    st.success("Affected Eye Correction: " + ", ".join(plan["affected_eye"]))
    if plan["other_eye"]:
        st.info("Other Eye Correction: " + ", ".join(plan["other_eye"]))

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    for idx, row in df.iterrows():
        st.markdown(f"### Case {idx + 1}")
        st.write(f"**Type**: {row['Deviation Type']} | **PD**: {row['Deviation (PD)']} | **Approach**: {row['Approach']}")
        plan = calculate_surgery(row['Deviation Type'], int(row['Deviation (PD)']), row['Approach'])
        display_plan(plan)

else:
    st.subheader("Manual Input")
    deviation_type = st.selectbox("Type of Deviation", ["Esotropia", "Exotropia", "Hypertropia", "Hypotropia"])
    deviation_value = st.number_input("Deviation (Prism Diopters)", min_value=15, step=5)
    approach = st.radio("Surgical Approach", ["Unilateral", "Bilateral"])

    if st.button("Show Recommendation"):
        plan = calculate_surgery(deviation_type, deviation_value, approach)
        display_plan(plan)
