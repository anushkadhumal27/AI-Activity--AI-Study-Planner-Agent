import ollama


def generate_study_plan(subjects, days, hours_per_day):

    prompt = f"""
Create a simple study timetable.

Subjects:
{subjects}

Days:
{days}

Study hours per day:
{hours_per_day}

Rules:
- Divide time fairly between subjects.
- Give extra time to difficult subjects.
- Include revision.
- Include practice.
- Include a mock test near the exam.
- Never exceed {hours_per_day} hours per day.

Keep the answer SHORT.

Use this format:

DAY 1
- Subject - Topic - Time
- Subject - Topic - Time

DAY 2
- Subject - Topic - Time
- Subject - Topic - Time

Continue until DAY {days}.

At the end give only 3 short exam tips.
"""

    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0.3,
            "num_predict": 1500
        }
    )

    return response["message"]["content"]