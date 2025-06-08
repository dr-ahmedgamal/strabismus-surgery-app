import streamlit as st
from logic import plan_unilateral

st.set_page_config(page_title="Strabismus Surgical Planner", layout="centered")
st.title("👁️ Strabismus Surgery Planning")

# --- Inputs ---
deviation_type = st.selectbox("Select deviation type:", ["Esotropia", "Exotropia", "Hypertropia", "Hypotropia"])

# Custom number input with + and - buttons
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

# --- Surgical Plan Button ---
surgical_plan_clicked = st.button("🧮 Surgical Plan", use_container_width=True)

result = None
switched_to_bilateral = False

if surgical_plan_clicked:
    if approach == "Unilateral":
        result = plan_unilateral(deviation_type, deviation_amount)
        if result.get("Switched to Bilateral"):
            st.warning("Unilateral correction not possible for this large deviation. Switching to bilateral approach.")
            switched_to_bilateral = True
    else:
        result = plan_unilateral(deviation_type, deviation_amount)
        if result.get("Switched to Bilateral"):
            switched_to_bilateral = True

    if result:
        st.subheader("Recommended Surgical Plan:")
        for k, v in result.items():
            if k != "Switched to Bilateral":
                st.write(f"🔹 **{k}**: {v} mm")
