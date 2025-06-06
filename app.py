import streamlit as st
import pandas as pd

# Load CSV
df = pd.read_csv("strabismus_nomogram.csv")

st.set_page_config(page_title="Strabismus Surgery Nomogram", layout="centered")

st.title("👁️ Strabismus Surgery Planner")
st.markdown("Enter the details below and click **Show Recommendation** to get the surgical plan.")

# Inputs
strabismus_type = st.selectbox("Strabismus Type", df["Strabismus_Type"].unique())
available_deviations = sorted(df["Deviation_PD"].unique())
deviation = st.selectbox("Deviation (in Prism Diopters)", available_deviations)
approach = st.radio("Surgical Approach", ["Unilateral", "Bilateral"])

# Function to check max correction for unilateral
def check_max_correction(sub_df):
    max_recession = sub_df["Recession_mm"].max()
    max_resection = sub_df["Resection_mm"].max()
    if max_recession > 12 or max_resection > 12:
        return False  # unilateral not suitable
    return True

# Function to generate bilateral corrections when needed
def generate_bilateral_plan(strabismus_type, deviation):
    # Filter for bilateral approach from data
    bilateral_df = df[
        (df["Strabismus_Type"] == strabismus_type) &
        (df["Deviation_PD"] == deviation) &
        (df["Approach"] == "Bilateral")
    ]
    return bilateral_df

def display_surgery(row):
    parts = []
    if row['Recession_mm'] > 0:
        parts.append(f"<b>{row['Recession_mm']} mm Recession</b>")
    if row['Resection_mm'] > 0:
        parts.append(f"<b>{row['Resection_mm']} mm Resection</b>")
    action = " | ".join(parts)
    if not action:
        return None
    return f"""
    <div style="font-size:18px; margin-bottom:10px;">
        <b>Muscle:</b> {row['Muscle']}<br>
        <b>Type:</b> {row['Surgery_Type']}<br>
        {action}
    </div>
    """

# Button trigger
if st.button("Show Recommendation"):

    # First, filter unilateral plan
    filtered_unilateral = df[
        (df["Strabismus_Type"] == strabismus_type) &
        (df["Deviation_PD"] == deviation) &
        (df["Approach"] == "Unilateral")
    ]

    # Check if unilateral plan fits max correction criteria
    if approach == "Unilateral" and not check_max_correction(filtered_unilateral):
        st.warning(
            "⚠️ Unilateral correction exceeds maximum 12 mm muscle correction. "
            "Switching to bilateral approach for safer and more effective treatment."
        )
        # Override approach to bilateral
        approach = "Bilateral"

    # Filter final plan
    filtered_df = df[
        (df["Strabismus_Type"] == strabismus_type) &
        (df["Deviation_PD"] == deviation) &
        (df["Approach"] == approach)
    ]

    if filtered_df.empty:
        st.warning("No surgical recommendation found for the selected values.")
    else:
        st.markdown("### 🩺 Recommended Surgical Plan:")

        if approach == "Unilateral":
            for idx, row in filtered_df.iterrows():
                surgery_plan = display_surgery(row)
                if surgery_plan:
                    st.markdown("**Affected Eye**", unsafe_allow_html=True)
                    st.markdown(surgery_plan, unsafe_allow_html=True)

        else:  # Bilateral
            half = len(filtered_df) // 2
            right_eye = filtered_df.iloc[:half]
            left_eye = filtered_df.iloc[half:]

            st.markdown("### 👁️ Right Eye")
            for idx, row in right_eye.iterrows():
                surgery_plan = display_surgery(row)
                if surgery_plan:
                    st.markdown(surgery_plan, unsafe_allow_html=True)

            st.markdown("### 👁️ Left Eye")
            for idx, row in left_eye.iterrows():
                surgery_plan = display_surgery(row)
                if surgery_plan:
                    st.markdown(surgery_plan, unsafe_allow_html=True)

else:
    st.info("Fill the form and click **Show Recommendation** to display results.")

st.markdown("---")
st.caption("Created to support precise ophthalmic strabismus surgical planning.")
