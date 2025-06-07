import streamlit as st
from logic import plan_unilateral, plan_bilateral

st.set_page_config(page_title="Strabismus Surgery Planner", layout="centered")

st.title("👁️‍🗨️ Strabismus Surgical Planning App")
st.markdown("This tool suggests surgical plans based on type and amount of strabismus.")

# User input
deviation_type = st.selectbox("Select deviation type:", ["Exotropia", "Esotropia", "Hypertropia", "Hypotropia"])
amount_pd = st.slider("Deviation amount (in prism diopters):", min_value=15, max_value=100, step=5)
approach = st.radio("Preferred approach:", ["Unilateral", "Bilateral"])

# Generate and display plan
st.subheader("📋 Recommended Surgical Plan:")

if approach == "Unilateral":
    plan = plan_unilateral(deviation_type, amount_pd)
    if "resection" not in " ".join(plan.keys()).lower():
        st.markdown("➡️ *Unilateral approach selected and feasible.*")
    else:
        st.markdown("🔁 *Unilateral not feasible — showing Bilateral plan.*")
else:
    plan = plan_bilateral(deviation_type, amount_pd)
    st.markdown("➡️ *Bilateral approach selected.*")

if plan:
    for key, value in plan.items():
        st.write(f"**{key}**: {value} mm")
else:
    st.warning("⚠️ No valid surgical plan found for the selected parameters.")
