import streamlit as st

from agent import generate_study_plan
from memory import save_memory, load_memory


# -----------------------------
# Page configuration
# -----------------------------

st.set_page_config(
    page_title="AI Study Planner",
    page_icon="🤖",
    layout="wide"
)


# -----------------------------
# Title
# -----------------------------

st.title("🤖 AI Study Planner Agent")

st.write(
    "Your intelligent study assistant that creates "
    "a personalized exam preparation plan."
)

st.divider()


# -----------------------------
# Student Information
# -----------------------------

st.header("👩‍🎓 Student Information")


name = st.text_input(
    "Enter your name"
)


subjects = st.text_area(
    "Enter your subjects",
    placeholder="Example:\nDSA\nJava\nDBMS"
)


days = st.number_input(
    "Days remaining before exam",
    min_value=1,
    max_value=365,
    value=20
)


hours = st.number_input(
    "Available study hours per day",
    min_value=1,
    max_value=12,
    value=3
)


# -----------------------------
# Generate Plan
# -----------------------------

if st.button(
    "🚀 Generate My Study Plan",
    type="primary"
):

    if not name:
        st.warning("Please enter your name.")

    elif not subjects:
        st.warning("Please enter your subjects.")

    else:

        with st.spinner(
            "🤖 AI Agent is creating your personalized plan..."
        ):

            try:
                plan = generate_study_plan(
                subjects,
                days,
                hours
                )

                study_data = {
                "name": name,
                "subjects": subjects,
                "days": days,
                "hours_per_day": hours,
                "plan": plan
                }

                save_memory(study_data)

                st.success(
                    "Your study plan has been created!"
                )

                st.divider()

                st.header("📚 Your Personalized Study Plan")

                st.markdown(plan)

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )
