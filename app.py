import streamlit as st
import pandas as pd

# Load the updated CSV file
df = pd.read_csv("strabismus_nomogram.csv")

st.title("👀 Strabismus Surgery Planner")
st.markdown("Enter the details below to get the recommended surgical plan:")

# User input
strabismus_type = st.selectbox("Strabismus Type", df["Strabismus_Type"].unique())
deviation = st.slider("Deviation (in Prism Diopters)", min_value=15, max_value=90, step=5)
approach = st.radio("Surgical Approach", ["Unilateral", "Bilateral"])

# Filter the dataset
filtered_df = df[
    (df["Strabismus_Type"] == strabismus_type) &
    (df["Deviation_PD"] == deviation) &
    (df["Approach"] == approach)
]

# Display results
st.subheader("Recommended Surgical Plan:")

def display_surgery(row):
    parts = []
    if row['Recession_mm'] > 0:
        parts.append(f"{row['Recession_mm']} mm Recession")
    if row['Resection_mm'] > 0:
        parts.append(f"{row['Resection_mm']} mm Resection")
    action = " | ".join(parts)
    return f"- Muscle: `{row['Muscle']}`\n  - Surgery Type: `{row['Surgery_Type']}`\n  - {action}" if action else None

if filtered_df.empty:
    st.warning("No surgical recommendation found for the selected values.")
else:
    if approach == "Unilateral":
        for idx, row in filtered_df.iterrows():
            surgery_plan = display_surgery(row)
            if surgery_plan:
                st.markdown("**Affected Eye**")
                st.markdown(surgery_plan)
    else:
        half = len(filtered_df) // 2
        right_eye = filtered_df.iloc[:half]
        left_eye = filtered_df.iloc[half:]

        st.markdown("### Right Eye")
        for idx, row in right_eye.iterrows():
            surgery_plan = display_surgery(row)
            if surgery_plan:
                st.markdown(surgery_plan)

        st.markdown("### Left Eye")
        for idx, row in left_eye.iterrows():
            surgery_plan = display_surgery(row)
            if surgery_plan:
                st.markdown(surgery_plan)

st.markdown("---")
st.caption("Built for ophthalmologists to assist in strabismus surgical planning.")
