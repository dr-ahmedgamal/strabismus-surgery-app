import streamlit as st
from logic import plan_unilateral

st.set_page_config(page_title="Strabismus Surgical Planner", layout="centered")
st.title("👁️ Strabismus Surgery Planning")

# --- Inputs ---
deviation_type = st.selectbox("Select deviation type:", ["Esotropia", "Exotropia", "Hypertropia", "Hypotropia"])

# Custom deviation input with + / - buttons
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    decrease = st.button("➖", key="dec")
with col3:
    increase = st.button("➕", key="inc")

if "deviation_amount" not in st.session_state:
    st.session_state["deviation_amount"] = 15

if increase:
    st.session_state["deviation_amount"] += 5
if decrease and st.session_state["deviation_amount"] > 5:
    st.session_state["deviation_amount"] -= 5

with col2:
    st.markdown(f"<h3 style='text-align: center;'>Deviation: {st.session_state['deviation_amount']} PD</h3>", unsafe_allow_html=True)

deviation_amount = st.session_state["deviation_amount"]

approach = st.radio("Preferred surgical approach:", ["Unilateral", "Bilateral"])

# --- Custom CSS to enlarge and style the button ---
st.markdown(
    """
    <style>
    div.stButton > button {
        height: 3.5em;
        width: 100%;
        font-size: 1.5em;
        font-weight: bold;
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# --- Large Surgical Plan Button ---
surgical_plan_clicked = st.button("Surgical Plan")

result = None
switched_to_bilateral = False

if surgical_plan_clicked:
    if approach == "Unilateral":
        result = plan_unilateral(deviation_type, deviation_amount)
        if isinstance(result, tuple):  # This means it switched to bilateral
            result, _ = result
            st.warning("Unilateral correction not possible for this large deviation. Switched to bilateral approach.")
            switched_to_bilateral = True
    else:
        result = plan_unilateral(deviation_type, deviation_amount)
        if isinstance(result, tuple):
            result, _ = result
            switched_to_bilateral = True

    if result:
        st.subheader("Recommended Surgical Plan:")
        for k, v in result.items():
            if k != "approach":
                st.write(f"🔹 **{k}**: {v} mm")
