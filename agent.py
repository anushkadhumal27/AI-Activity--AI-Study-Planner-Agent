import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY", "").strip()

if not api_key:
    raise RuntimeError(
        "GROQ_API_KEY was not found. Add GROQ_API_KEY to your .env file."
    )

client = Groq(api_key=api_key)
MODEL = "openai/gpt-oss-20b"


def _get_response(prompt, max_tokens=1500):
    """Get only the model's final answer.

    GPT-OSS is a reasoning model. If reasoning is allowed to consume the
    whole completion budget, message.content can be empty. We explicitly
    disable reasoning output and use max_completion_tokens so the application
    always receives the text that Streamlit should display.
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_completion_tokens=max_tokens,
        reasoning_effort="low",
        include_reasoning=False,
    )

    if not response.choices:
        raise RuntimeError("The AI model returned no response.")

    content = response.choices[0].message.content

    if content is None or not str(content).strip():
        raise RuntimeError(
            "The AI model returned an empty answer. Please click the button again."
        )

    return str(content).strip()


def generate_study_plan(subjects, days, hours_per_day):
    prompt = f"""
You are an AI Study Planner Agent.

Create a realistic study timetable for a student.

Subjects:
{subjects}

Days remaining:
{days}

Available study hours per day:
{hours_per_day}

Rules:
- Distribute the available time among all subjects.
- Include revision.
- Include practice sessions.
- Include a mock test near the exam.
- Do not exceed the available study hours per day.
- Keep the answer short and easy to understand.
- Use all subjects provided by the student.

Format:

DAY 1
- Subject - Topic - Duration

DAY 2
- Subject - Topic - Duration

Continue until DAY {days}.

At the end give 3 short exam tips.
"""

    return _get_response(prompt, max_tokens=2500)


def reschedule_study_plan(
    current_plan,
    missed_session,
    days_remaining,
    hours_per_day,
):
    prompt = f"""
You are an AI Study Planner Agent.

A student has reported missed study time:
{missed_session}

CURRENT STUDY PLAN:
{current_plan}

TOTAL EXAM PREPARATION DAYS:
{days_remaining}

AVAILABLE STUDY HOURS PER DAY:
{hours_per_day}

Your instructions:
1. Carefully analyze the current study plan and the missed study details.
2. Formulate the COMPLETE updated study timetable for all relevant days up to Day {days_remaining} without exceeding {hours_per_day} study hours per day.
3. Identify ONLY the study sessions that were actually changed, added, or shifted to absorb the missed material (do not list unchanged days or unchanged topics).

You MUST format your response into EXACTLY TWO separated sections using these exact delimiter tags:

---RESCHEDULING_RESULT---
RESCHEDULED_DAYS:
Day <X>
- <Subject> – <Topic>
- Added/shifted <duration>

Day <Y>
- <Subject> – <Topic>
- Added/shifted <duration>

ADDED_SHIFTED_PLAN:
- Day <X> → <Subject> – <Topic> — <duration>
- Day <Y> → <Subject> – <Topic> — <duration>

REASON:
<One concise sentence explaining how the missed session was redistributed across the specified days while keeping the daily study limit within {hours_per_day} hours.>
---END_RESCHEDULING_RESULT---

---UPDATED_STUDY_PLAN---
UPDATED STUDY PLAN

DAY 1
- Subject - Topic - Duration

DAY 2
- Subject - Topic - Duration

Continue for all relevant days up to DAY {days_remaining}.
---END_UPDATED_STUDY_PLAN---
"""

    response_text = _get_response(prompt, max_tokens=3200)

    rescheduling_info = {
        "rescheduled_days": "",
        "added_shifted_plan": "",
        "reason": "",
    }
    updated_plan = ""

    if "---RESCHEDULING_RESULT---" in response_text and "---END_RESCHEDULING_RESULT---" in response_text:
        summary_block = (
            response_text.split("---RESCHEDULING_RESULT---")[1]
            .split("---END_RESCHEDULING_RESULT---")[0]
            .strip()
        )

        if "RESCHEDULED_DAYS:" in summary_block:
            part = summary_block.split("RESCHEDULED_DAYS:")[1]
            for stop in ["ADDED_SHIFTED_PLAN:", "REASON:"]:
                if stop in part:
                    part = part.split(stop)[0]
            rescheduling_info["rescheduled_days"] = part.strip()

        if "ADDED_SHIFTED_PLAN:" in summary_block:
            part = summary_block.split("ADDED_SHIFTED_PLAN:")[1]
            if "REASON:" in part:
                part = part.split("REASON:")[0]
            rescheduling_info["added_shifted_plan"] = part.strip()

        if "REASON:" in summary_block:
            part = summary_block.split("REASON:")[1].strip()
            rescheduling_info["reason"] = part.strip()

    if "---UPDATED_STUDY_PLAN---" in response_text:
        plan_block = response_text.split("---UPDATED_STUDY_PLAN---")[1]
        if "---END_UPDATED_STUDY_PLAN---" in plan_block:
            plan_block = plan_block.split("---END_UPDATED_STUDY_PLAN---")[0]
        updated_plan = plan_block.strip()
    else:
        updated_plan = response_text.strip()

    return {
        "updated_plan": updated_plan if updated_plan else response_text.strip(),
        "rescheduling_info": rescheduling_info,
        "raw_response": response_text.strip(),
    }


def study_assistant(question, student_data):
    name = student_data.get("name", "Student")
    subjects = student_data.get("subjects", "")
    if isinstance(subjects, list):
        subjects = ", ".join(str(s) for s in subjects)
    days = student_data.get("days", 1)
    hours = student_data.get("hours_per_day", 1)
    plan = student_data.get("plan", "No study plan available.")
    updated_plan = student_data.get("updated_plan", "None") or "None"
    try:
        progress = float(student_data.get("progress", 0) or 0)
    except (ValueError, TypeError):
        progress = 0.0
    completed_sessions = student_data.get("completed_sessions", {})
    missed_session = student_data.get("last_missed_session", "None") or "None"

    prompt = f"""
You are an intelligent AI Study Assistant.

Student name: {name}

SUBJECTS:
{subjects}

DAYS REMAINING:
{days}

AVAILABLE STUDY HOURS PER DAY:
{hours}

ORIGINAL STUDY PLAN:
{plan}

UPDATED PLAN, IF ANY:
{updated_plan}

OVERALL PROGRESS:
{progress:.1f}%

COMPLETED SESSIONS:
{completed_sessions}

LAST MISSED SESSION:
{missed_session}

STUDENT QUESTION:
{question}

Instructions:
- Answer the student's question clearly and concisely.
- Use the student's actual plan and progress.
- Give practical study advice.
- Do not invent progress information.
- If asked what to study, use the current plan.
- If an updated plan exists, use it when relevant.
- If the student has limited time, prioritize the most important work.

Answer the student directly.
"""

    return _get_response(prompt, max_tokens=1200)
