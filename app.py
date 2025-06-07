import streamlit as st
from logic import plan_unilateral, plan_bilateral

st.set_page_config(page_title="Strabismus Planner", layout="centered")

st.title("👁️ Strabismus Surgical Planner")
st.markdown("Enter deviation type and amount to generate an optimal surgical plan.")

# Input
deviation_type = st.selectbox("Deviation type:", ["Exotropia", "Esotropia", "Hypertropia", "Hypotropia"])
amount_pd = st.slider("Deviation (PD):", 15, 100, step=5)
approach = st.radio("Preferred approach:", ["Unilateral", "Bilateral"])

# Compute plan
st.subheader("📋 Surgical Plan:")

if approach == "Unilateral":
    plan, converted = plan_unilateral(deviation_type, amount_pd)
    if converted:
        st.markdown("⚠️ *Unilateral approach not feasible — switched to Bilateral.*")
    else:
        st.markdown("✅ *Unilateral approach used.*")
else:
    plan = plan_bilateral(deviation_type, amount_pd)
    st.markdown("✅ *Bilateral approach used.*")

# Show results
if plan:
    for step, mm in plan.items():
        st.write(f"**{step}**: {mm} mm")
else:
    st.error("No valid surgical plan could be generated.")
