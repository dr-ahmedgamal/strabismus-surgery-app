import streamlit as st
from logic import calculate_surgery

def main():
    st.title("Strabismus Surgical Planner")

    # Dropdown for deviation type
    deviation_type = st.selectbox(
        "Select Deviation Type:",
        ("Esotropia", "Exotropia", "Hypertropia", "Hypotropia")
    )

    # Dropdown for deviation amount starting at 15, step 5, max 80 or 100 as you want
    deviation_values = list(range(15, 101, 5))
    deviation_value = st.selectbox("Select Deviation (prism diopters):", deviation_values, index=0)

    approach = st.radio("Choose Surgical Approach:", ("Unilateral", "Bilateral"))

    if st.button("Get Surgical Recommendation"):
        plan = calculate_surgery(deviation_type, deviation_value, approach)

        # Separate procedures by eye
        affected_eye = []
        contralateral_eye = []

        for eye, procedure in plan:
            if eye == "Affected Eye":
                affected_eye.append(procedure)
            else:
                contralateral_eye.append(procedure)

        # Format output
        st.subheader("Surgical Recommendation")
        if affected_eye:
            st.markdown("**Affected Eye Correction:**  ")
            st.markdown(", ".join(affected_eye))

        if contralateral_eye:
            st.markdown("**Contralateral Eye Correction:**  ")
            st.markdown(", ".join(contralateral_eye))


if __name__ == "__main__":
    main()
