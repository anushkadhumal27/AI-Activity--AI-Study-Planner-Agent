import streamlit as st

from agent import (
    generate_study_plan,
    reschedule_study_plan,
    study_assistant
)

from memory import save_memory, load_memory, clear_memory

# =========================================
# HELPER FUNCTIONS
# =========================================

def parse_subjects(subjects_data):
    """Return a clean list of subject names from string or list input."""
    if isinstance(subjects_data, list):
        return [str(s).strip() for s in subjects_data if str(s).strip()]
    elif isinstance(subjects_data, str):
        return [s.strip() for s in subjects_data.splitlines() if s.strip()]
    return []


def format_subjects_text(subjects_data):
    """Format subjects as newline-separated text for input areas."""
    if isinstance(subjects_data, list):
        return "\n".join(str(s).strip() for s in subjects_data if str(s).strip())
    elif isinstance(subjects_data, str):
        return subjects_data
    return ""


def sync_to_memory():
    """Helper to save current application state to disk memory."""
    if not st.session_state.get("student_data"):
        return

    active_plan = st.session_state.get("updated_plan") or st.session_state.get("original_plan", "")

    data_to_save = {
        "name": st.session_state.student_data.get("name", ""),
        "subjects": st.session_state.student_data.get("subjects", ""),
        "days": int(st.session_state.student_data.get("days", 1)),
        "hours_per_day": int(st.session_state.student_data.get("hours_per_day", 1)),
        "plan": active_plan,
        "updated_plan": st.session_state.get("updated_plan", ""),
        "completed_sessions": st.session_state.get("completed_sessions", {}),
        "last_missed_session": st.session_state.get("last_missed_session", ""),
        "progress": float(st.session_state.get("overall_progress", 0.0)),
        "module3_reschedule_result": st.session_state.get("module3_reschedule_result", None),
    }
    save_memory(data_to_save)


# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="AI Study Planner",
    page_icon="🤖",
    layout="wide",
)

# =========================================
# STYLING
# =========================================

st.markdown("""
<style>
.hero {
    padding: 45px 30px;
    margin: 20px 0 35px 0;
    text-align: center;
    background: linear-gradient(135deg, #111827, #312e81);
    border-radius: 24px;
    box-shadow: 0 15px 35px rgba(31, 41, 55, 0.18);
}
.hero h1 {
    margin: 0;
    color: white;
    font-size: 42px;
    font-weight: 800;
}
.hero p {
    margin-top: 14px;
    color: #c7d2fe;
    font-size: 17px;
}
</style>

<div class="hero">
    <h1>🤖 AI Study Planner Agent</h1>
    <p>
        Your intelligent study assistant that creates
        a personalized exam preparation plan.
    </p>
</div>
""", unsafe_allow_html=True)

# =========================================
# SESSION STATE INITIALIZATION & MEMORY SYNC
# =========================================

if "initialized" not in st.session_state:
    saved = load_memory()
    has_saved_plan = bool(saved.get("plan") or saved.get("updated_plan"))

    if saved.get("name") and has_saved_plan:
        st.session_state.student_data = {
            "name": saved.get("name", ""),
            "subjects": saved.get("subjects", ""),
            "days": int(saved.get("days", 20)),
            "hours_per_day": int(saved.get("hours_per_day", 3)),
        }
        st.session_state.original_plan = saved.get("plan", "")
        st.session_state.updated_plan = saved.get("updated_plan", "")
        st.session_state.module3_updated_plan = saved.get("updated_plan", "")
        st.session_state.completed_sessions = saved.get("completed_sessions", {})
        st.session_state.last_missed_session = saved.get("last_missed_session", "")
        st.session_state.module3_reschedule_result = saved.get("module3_reschedule_result", None)
        st.session_state.overall_progress = float(saved.get("progress", 0.0))
    else:
        st.session_state.student_data = None
        st.session_state.original_plan = ""
        st.session_state.updated_plan = ""
        st.session_state.module3_updated_plan = ""
        st.session_state.completed_sessions = {}
        st.session_state.last_missed_session = ""
        st.session_state.module3_reschedule_result = None
        st.session_state.overall_progress = 0.0

    st.session_state.assistant_messages = []
    st.session_state.initialized = True

    # Pre-populate session checkbox states from loaded memory
    if isinstance(st.session_state.completed_sessions, dict):
        for s_id, is_done in st.session_state.completed_sessions.items():
            try:
                parts = s_id.split(" - ", 1)
                day_num = parts[0].replace("Day ", "").strip()
                subj = parts[1].strip()
                st.session_state[f"session_{day_num}_{subj}"] = bool(is_done)
            except Exception:
                pass

if "student_data" not in st.session_state:
    st.session_state.student_data = None

if "original_plan" not in st.session_state:
    st.session_state.original_plan = ""

if "updated_plan" not in st.session_state:
    st.session_state.updated_plan = ""

if "module3_updated_plan" not in st.session_state:
    st.session_state.module3_updated_plan = ""

if "completed_sessions" not in st.session_state:
    st.session_state.completed_sessions = {}

if "last_missed_session" not in st.session_state:
    st.session_state.last_missed_session = ""

if "module3_reschedule_result" not in st.session_state:
    st.session_state.module3_reschedule_result = None

if "assistant_messages" not in st.session_state:
    st.session_state.assistant_messages = []

# =========================================
# SIDEBAR CONTROLS
# =========================================

with st.sidebar:
    st.header("⚙️ Study Planner Controls", anchor=False)
    if st.session_state.student_data:
        st.success(f"👤 **Student**: {st.session_state.student_data.get('name', 'Student')}")
        status_label = "Rescheduled Plan Active ⚡" if st.session_state.updated_plan else "Original Plan Active 📚"
        st.info(f"**Status**: {status_label}")
        if st.session_state.last_missed_session:
            st.caption(f"Last Missed: {st.session_state.last_missed_session}")

    if st.button("🗑️ Reset & Start Fresh", help="Clear all stored study plans and progress"):
        clear_memory()
        for k in list(st.session_state.keys()):
            del st.session_state[k]
        st.rerun()

# =========================================
# MODULE 1 - AI STUDY PLAN GENERATOR
# =========================================

st.header("📅 Module 1: AI Study Plan Generator", anchor=False)

default_name = st.session_state.student_data.get("name", "") if st.session_state.student_data else ""
default_subjects = format_subjects_text(st.session_state.student_data.get("subjects", "")) if st.session_state.student_data else ""
default_days = int(st.session_state.student_data.get("days", 20)) if st.session_state.student_data else 20
default_hours = int(st.session_state.student_data.get("hours_per_day", 3)) if st.session_state.student_data else 3

name = st.text_input("Enter your name", value=default_name)

subjects = st.text_area(
    "Enter your subjects",
    value=default_subjects,
    placeholder="Example:\nDSA\nJava\nDBMS",
)

days = st.number_input(
    "Days remaining before exam",
    min_value=1,
    max_value=365,
    value=default_days,
)

hours = st.number_input(
    "Available study hours per day",
    min_value=1,
    max_value=12,
    value=default_hours,
)

if st.button("🚀 Generate My Study Plan", type="primary", key="generate_plan"):
    if not name.strip():
        st.warning("Please enter your name.")
    elif not subjects.strip():
        st.warning("Please enter your subjects.")
    else:
        with st.spinner("🤖 AI Agent is creating your personalized plan..."):
            try:
                plan = generate_study_plan(subjects, days, hours)

                st.session_state.student_data = {
                    "name": name.strip(),
                    "subjects": subjects.strip(),
                    "days": int(days),
                    "hours_per_day": int(hours),
                }

                st.session_state.original_plan = plan
                st.session_state.updated_plan = ""
                st.session_state.module3_updated_plan = ""
                st.session_state.completed_sessions = {}
                st.session_state.last_missed_session = ""
                st.session_state.module3_reschedule_result = None
                st.session_state.assistant_messages = []
                st.session_state.overall_progress = 0.0

                # Clear old checkbox states from session_state
                for k in list(st.session_state.keys()):
                    if k.startswith("session_"):
                        del st.session_state[k]

                # Persist to disk memory
                sync_to_memory()

                st.success("Your study plan has been created! 🧠")

            except Exception as e:
                st.error(f"Something went wrong: {e}")

if st.session_state.original_plan:
    st.divider()
    display_plan = st.session_state.updated_plan or st.session_state.original_plan
    plan_title = (
        "⚡ Active Rescheduled Plan"
        if st.session_state.updated_plan
        else "📚 Your Personalized Study Plan"
    )
    st.subheader(plan_title, anchor=False)
    if st.session_state.updated_plan and st.session_state.last_missed_session:
        st.info(f"Adjusted for missed session: **{st.session_state.last_missed_session}**")
    st.markdown(display_plan)

# =========================================
# MODULE 2 - AUTOMATIC PROGRESS TRACKER
# =========================================

st.divider()
st.header("📊 Module 2: Automatic Study Progress Tracker", anchor=False)

student_data = st.session_state.student_data

if student_data and (st.session_state.original_plan or st.session_state.updated_plan):
    student_name = student_data.get("name", "Student")
    subject_list = parse_subjects(student_data.get("subjects", ""))
    total_days = int(student_data.get("days", 1))

    st.write(f"Track your completed study sessions, **{student_name}**.")
    st.subheader("📚 Complete Your Study Sessions", anchor=False)

    total_sessions = len(subject_list) * total_days
    completed_count = 0

    for subject in subject_list:
        st.markdown(f"### 📖 {subject}")

        for day in range(1, total_days + 1):
            session_id = f"Day {day} - {subject}"
            key = f"session_{day}_{subject}"

            # Ensure session state has the current value
            if key not in st.session_state:
                st.session_state[key] = bool(
                    st.session_state.completed_sessions.get(session_id, False)
                )

            is_completed = st.checkbox(
                f"Day {day} — {subject} session completed",
                key=key,
            )

            st.session_state.completed_sessions[session_id] = is_completed

            if is_completed:
                completed_count += 1

    overall_progress = (
        (completed_count / total_sessions) * 100
        if total_sessions else 0.0
    )
    st.session_state.overall_progress = overall_progress

    # Sync progress to persistent disk memory
    sync_to_memory()

    st.divider()
    st.subheader("📈 Your Progress", anchor=False)
    progress_val = min(max(float(overall_progress) / 100.0, 0.0), 1.0)
    st.progress(progress_val)
    st.write(f"### Overall Progress: {overall_progress:.1f}%")
    st.write(f"Completed sessions: **{completed_count} / {total_sessions}**")

    st.subheader("📊 Subject-wise Progress", anchor=False)

    for subject in subject_list:
        subject_completed = sum(
            1
            for day in range(1, total_days + 1)
            if st.session_state.completed_sessions.get(
                f"Day {day} - {subject}", False
            )
        )

        subject_progress = (
            (subject_completed / total_days) * 100
            if total_days else 0.0
        )
        subj_val = min(max(float(subject_progress) / 100.0, 0.0), 1.0)

        st.write(f"**{subject}: {subject_progress:.1f}%** ({subject_completed}/{total_days} sessions)")
        st.progress(subj_val)

else:
    st.info("Please generate a study plan first.")

# =========================================
# MODULE 3 - AI MISSED SESSION RESCHEDULER
# =========================================

st.divider()
st.header("🔄 Module 3: AI Missed Session Rescheduler", anchor=False)

# Use session state as primary, fallback to load_memory if needed
active_plan = st.session_state.get("updated_plan") or st.session_state.get("original_plan")
active_student = st.session_state.get("student_data")

if not active_student or not active_plan:
    # Check if data exists in memory file
    mem_data = load_memory()
    if mem_data.get("plan") or mem_data.get("updated_plan"):
        active_plan = mem_data.get("updated_plan") or mem_data.get("plan")
        active_student = {
            "name": mem_data.get("name", "Student"),
            "subjects": mem_data.get("subjects", ""),
            "days": int(mem_data.get("days", 1)),
            "hours_per_day": int(mem_data.get("hours_per_day", 1)),
        }
        st.session_state.student_data = active_student
        st.session_state.original_plan = mem_data.get("plan", "")
        st.session_state.updated_plan = mem_data.get("updated_plan", "")
        st.session_state.module3_updated_plan = mem_data.get("updated_plan", "")

if not active_student or not active_plan:
    st.info("Please generate a study plan first.")
else:
    st.write(
        "Missed study sessions or fell behind? Let the AI automatically "
        "rebalance your remaining timetable and build an actionable catch-up strategy."
    )

    st.subheader("❌ Report Missed Study Time", anchor=False)

    subject_list = parse_subjects(active_student.get("subjects", ""))
    total_days = int(active_student.get("days", 1))
    hours_per_day = int(active_student.get("hours_per_day", 1))

    missed_mode = st.radio(
        "How much study time did you miss?",
        [
            "Single Session (1 day / 1 topic)",
            "Multiple Days (More than 1 day missed)"
        ],
        key="module3_missed_mode",
        horizontal=True,
    )

    missed_session_summary = ""

    if missed_mode == "Single Session (1 day / 1 topic)":
        col_day, col_subj = st.columns(2)
        with col_day:
            missed_day = st.selectbox(
                "Which day did you miss?",
                list(range(1, total_days + 1)),
                key="module3_missed_day"
            )
        with col_subj:
            missed_subject = st.selectbox(
                "Which subject did you miss?",
                subject_list if subject_list else ["General"],
                key="module3_missed_subject"
            )

        missed_topic = st.text_input(
            "What topic did you miss?",
            placeholder="Example: OOP Concepts / Binary Trees",
            key="module3_missed_topic"
        )

        if missed_topic.strip():
            missed_session_summary = (
                f"Single session missed: Day {missed_day} - {missed_subject} - {missed_topic.strip()}"
            )
            st.markdown(f"**Missed:**  \nDay {missed_day} — {missed_subject} — {missed_topic.strip()}")
    else:
        # Multiple days missed
        st.info("💡 When multiple days are missed, the AI will redistribute the backlog across the remaining days without exceeding your daily study hours.")

        selected_days = st.multiselect(
            "Select all the days you missed (more than 1 day):",
            options=list(range(1, total_days + 1)),
            default=[1, 2] if total_days >= 2 else [1],
            key="module3_multi_days"
        )

        selected_subjects = st.multiselect(
            "Which subjects were affected during these missed days?",
            options=subject_list,
            default=subject_list,
            key="module3_multi_subjects"
        )

        missed_reason_or_topics = st.text_input(
            "Specific topics missed or reason for absence (optional):",
            placeholder="Example: Missed all sessions due to illness / family event",
            key="module3_multi_notes"
        )

        if selected_days:
            sorted_days = sorted(selected_days)
            days_str = ", ".join(f"Day {d}" for d in sorted_days)
            subjects_str = ", ".join(selected_subjects) if selected_subjects else "All scheduled subjects"
            notes_str = f" | Notes/Topics: {missed_reason_or_topics.strip()}" if missed_reason_or_topics.strip() else ""
            missed_session_summary = (
                f"MULTIPLE DAYS MISSED ({len(sorted_days)} days): {days_str} | "
                f"Affected Subjects: {subjects_str}{notes_str}"
            )
            notes_disp = f" — {missed_reason_or_topics.strip()}" if missed_reason_or_topics.strip() else ""
            st.markdown(f"**Missed:**  \n{days_str} — {subjects_str}{notes_disp}")

    if st.button(
        "🔄 Reschedule With AI",
        type="primary",
        key="module3_reschedule"
    ):
        if missed_mode == "Single Session (1 day / 1 topic)" and not missed_topic.strip():
            st.warning("Please enter the missed topic.")
        elif missed_mode != "Single Session (1 day / 1 topic)" and not selected_days:
            st.warning("Please select at least 1 day that you missed.")
        else:
            with st.spinner("🤖 AI is analyzing the backlog and rearranging your study plan..."):
                try:
                    # Current plan to reschedule is the latest active plan
                    current_plan_to_reschedule = (
                        st.session_state.get("updated_plan")
                        or st.session_state.get("original_plan")
                        or active_plan
                    )

                    updated_plan_result = reschedule_study_plan(
                        current_plan_to_reschedule,
                        missed_session_summary,
                        total_days,
                        hours_per_day,
                    )

                    if isinstance(updated_plan_result, dict):
                        cleaned_plan = str(updated_plan_result.get("updated_plan", "")).strip()
                        rescheduling_info = updated_plan_result.get("rescheduling_info", {})
                    else:
                        cleaned_plan = str(updated_plan_result).strip()
                        rescheduling_info = {}

                    if not cleaned_plan:
                        st.error(
                            "The AI returned an empty updated plan. Please try again."
                        )
                    else:
                        # Fallback for display if any section is empty
                        if not rescheduling_info.get("rescheduled_days"):
                            if missed_mode == "Single Session (1 day / 1 topic)":
                                new_d = min(missed_day + 2, total_days)
                                rescheduling_info["rescheduled_days"] = f"Day {new_d}\n- {missed_subject} – {missed_topic.strip()}\n- Added 1 hour"
                                rescheduling_info["added_shifted_plan"] = f"- Day {new_d} → {missed_subject} – {missed_topic.strip()} — 1 hour"
                                rescheduling_info["reason"] = f"The missed {missed_topic.strip()} session was redistributed to Day {new_d} by shifting available study time while keeping the daily study limit within {hours_per_day} hours."
                            else:
                                lines_days = []
                                lines_added = []
                                for idx, s in enumerate(selected_subjects or subject_list):
                                    d_target = min(max(selected_days) + 1 + idx, total_days)
                                    lines_days.append(f"Day {d_target}\n- {s}\n- Added/shifted 1 hour")
                                    lines_added.append(f"- Day {d_target} → {s} — 1 hour")
                                rescheduling_info["rescheduled_days"] = "\n\n".join(lines_days)
                                rescheduling_info["added_shifted_plan"] = "\n".join(lines_added)
                                rescheduling_info["reason"] = f"The missed sessions were redistributed across remaining study days by shifting available study time while keeping the daily study limit within {hours_per_day} hours."

                        # Store into session state (both keys for compatibility)
                        st.session_state.updated_plan = cleaned_plan
                        st.session_state.module3_updated_plan = cleaned_plan
                        st.session_state.last_missed_session = missed_session_summary
                        st.session_state.module3_reschedule_result = rescheduling_info

                        # Persist to disk memory
                        sync_to_memory()

                        st.success(
                            "Your study plan has been successfully rescheduled! ✅"
                        )

                except Exception as e:
                    st.error(f"Something went wrong: {e}")

# =========================================
# DISPLAY ONLY 3 RESCHEDULING SECTIONS IN MODULE 3
# =========================================
resched_res = st.session_state.get("module3_reschedule_result")
if resched_res:
    st.divider()

    st.subheader("🔄 Rescheduled Days", anchor=False)
    st.markdown(resched_res.get("rescheduled_days", ""))

    st.subheader("➕ Added / Shifted Plan", anchor=False)
    st.markdown(resched_res.get("added_shifted_plan", ""))

    st.subheader("💡 Reason", anchor=False)
    st.markdown(resched_res.get("reason", ""))

# =========================================
# MODULE 4 - AI STUDY ASSISTANT
# =========================================

st.divider()
st.header("💬 Module 4: AI Study Assistant", anchor=False)

student_data = st.session_state.student_data
has_plan = bool(st.session_state.original_plan or st.session_state.updated_plan)

if student_data and has_plan:
    st.write(
        "Ask your AI assistant anything about your study plan, "
        "progress, or preparation."
    )

    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🗑️ Clear Chat", key="clear_chat", help="Clear conversation history"):
            st.session_state.assistant_messages = []
            st.rerun()

    # Display existing chat messages
    for message in st.session_state.assistant_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask your study assistant...")

    if question:
        st.session_state.assistant_messages.append({
            "role": "user",
            "content": question,
        })

        with st.chat_message("user"):
            st.markdown(question)

        # Compute accurate progress
        completed = st.session_state.completed_sessions
        subject_list = parse_subjects(student_data.get("subjects", ""))
        total_days = int(student_data.get("days", 1))
        total_sessions = len(subject_list) * total_days
        completed_count = sum(1 for v in completed.values() if v)
        progress = (
            (completed_count / total_sessions) * 100.0
            if total_sessions else 0.0
        )

        assistant_data = {
            **student_data,
            "plan": st.session_state.original_plan,
            "updated_plan": st.session_state.updated_plan or "None",
            "progress": progress,
            "completed_sessions": completed,
            "last_missed_session": st.session_state.get("last_missed_session") or "None",
        }

        with st.chat_message("assistant"):
            with st.spinner("🤖 Thinking..."):
                try:
                    answer = study_assistant(question, assistant_data)
                    st.markdown(answer)

                    st.session_state.assistant_messages.append({
                        "role": "assistant",
                        "content": answer,
                    })
                except Exception as e:
                    st.error(f"Something went wrong: {e}")
else:
    st.info("Please generate a study plan first.")

