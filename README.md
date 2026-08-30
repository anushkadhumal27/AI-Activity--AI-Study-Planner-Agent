# AI-Activity--AI-Study-Planner-Agent
AI Study Planner Agent is a Python-based application that uses Streamlit, Ollama, and Llama 3.2 to generate personalized study schedules. It considers subjects, available study hours, and exam time, while using JSON memory to save plans for future use.


# 🤖 AI Study Planner Agent

An intelligent study-planning application using **Python, Streamlit, Ollama, and Llama 3.2** to generate personalized study schedules. The project also includes a simple **JSON-based memory system** for saving generated plans.

## 📌 Project Overview

The AI Study Planner Agent helps students create personalized study timetables based on:

- Student name
- Subjects
- Number of days remaining before the examination
- Available study hours per day
- Revision requirements
- Practice requirements

The AI analyzes these inputs and generates a suitable **day-by-day study plan**.

The project is designed as an **AI agent activity rather than a simple chatbot**, because it can maintain study-plan information and can be extended with progress tracking, missed-session detection, and automatic rescheduling. fileciteturn0file0L9-L22

## 🎯 Objectives

1. Develop an AI-based study planning system.
2. Create personalized study schedules.
3. Distribute available study hours among multiple subjects.
4. Include revision and practice sessions.
5. Provide exam-preparation recommendations.
6. Store generated study plans for future use.
7. Demonstrate the concept of an AI agent.
8. Provide a foundation for automatic rescheduling of missed sessions. fileciteturn0file0L44-L53

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| **Python** | Main programming language |
| **Streamlit** | User interface |
| **Ollama** | Local AI model execution |
| **Llama 3.2** | AI language model |
| **JSON** | Storing study-plan memory |
| **python-dotenv** | Environment configuration |
| **VS Code** | Development environment |

## 🏗️ System Architecture

```text
                 STUDENT
                    │
                    ▼
          ┌─────────────────┐
          │  Streamlit UI   │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │    AI Agent     │
          │    agent.py     │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │     Ollama      │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │    Llama 3.2    │
          │    Local AI     │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │ Generated Study │
          │      Plan       │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │   JSON Memory   │
          │study_memory.json│
          └─────────────────┘
```

This follows the architecture described in the project material. fileciteturn0file0L91-L133

## 🔄 How the System Works

### 1. Student enters information

Example:

```text
Name: Anushka

Subjects:
DSA
Java
DBMS

Days remaining: 7
Study hours per day: 3
```

### 2. AI Agent processes the information

The agent considers:

- Number of subjects
- Available study time
- Number of days
- Revision requirements
- Practice requirements

### 3. AI generates a schedule

Example:

```text
DAY 1

DSA - Arrays - 1 hour
Java - OOP - 1 hour
DBMS - SQL - 1 hour

DAY 2

DSA - Searching - 1 hour
Java - Inheritance - 1 hour
DBMS - Normalization - 1 hour
```

The exact schedule depends on the student's input. fileciteturn0file0L140-L203

### 4. Plan is displayed

The generated schedule is displayed in the Streamlit application.

### 5. Plan is stored

The plan is saved in:

```text
study_memory.json
```

This provides a basic memory mechanism. fileciteturn0file0L207-L226

## 🧠 AI Agent Behavior

The project is designed to support agentic behavior:

```text
Understand student information
            ↓
Analyze constraints
            ↓
Make planning decisions
            ↓
Generate a schedule
            ↓
Store the schedule
            ↓
Track future progress
            ↓
Modify the schedule when required
```

A future version can accept a request such as:

```text
"I missed yesterday's DSA session."
```

and then identify the missed session, check remaining study time, reschedule the topic, adjust the future schedule, and save the updated plan. fileciteturn0file0L230-L282

## 💾 Memory System

The project uses JSON as simple persistent memory.

Example:

```json
{
  "name": "Anushka",
  "subjects": "DSA
Java
DBMS",
  "days": 7,
  "hours_per_day": 3,
  "plan": "DAY 1..."
}
```

The saved information can be loaded when the application runs again. fileciteturn0file0L286-L305

## 🖥️ User Interface

The Streamlit interface provides:

- Student name
- Subjects
- Days remaining before the exam
- Available study hours per day
- **Generate My Study Plan** action

After clicking the button, the personalized plan is displayed. fileciteturn0file0L311-L333

## ▶️ Installation and Setup

### Prerequisites

- Python
- Streamlit
- Ollama
- Llama 3.2
- VS Code or another Python IDE

Internet is required initially for installation/model download according to the project requirements. fileciteturn0file0L71-L87

### 1. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

### 2. Install dependencies

If the project contains `requirements.txt`:

```bash
pip install -r requirements.txt
```

Otherwise:

```bash
pip install streamlit ollama python-dotenv
```

### 3. Prepare the local AI model

Install Ollama and make sure the Llama 3.2 model is available locally.

```bash
ollama pull llama3.2
```

### 4. Run the application

```bash
streamlit run app.py
```

## 📁 Project Structure

```text
HOD_Activity/
│
├── venv/
│
├── app.py
│   └── Streamlit user interface
│
├── agent.py
│   └── AI study planner
│
├── memory.py
│   └── Memory functions
│
├── study_memory.json
│   └── Saved study plan
│
└── .env
    └── Configuration file
```

The project structure is based on the provided activity documentation. fileciteturn0file0L522-L550

## ✅ Implemented Features

| Component | Status |
|---|---|
| Streamlit UI | ✅ |
| Student input | ✅ |
| AI study-plan generation | ✅ |
| Local Llama 3.2 model | ✅ |
| Ollama integration | ✅ |
| Study-plan memory | ✅ |
| JSON storage | ✅ |
| Progress tracking | 🔄 Future enhancement |
| Missed-session detection | 🔄 Future enhancement |
| Automatic rescheduling | 🔄 Future enhancement |
| Natural-language agent commands | 🔄 Future enhancement |

## ⭐ Advantages

- **Personalized planning**
- **Time management**
- **Revision support**
- **Practice support**
- **Local AI**
- **Memory**
- **Extendable agent architecture**

These advantages are described in the supplied project report. fileciteturn0file0L393-L410

## ⚠️ Limitations

1. Plan quality depends on the local AI model.
2. Local models may respond more slowly on limited hardware.
3. Memory currently uses a simple JSON file.
4. The current version does not automatically detect completed topics.
5. Automatic missed-session rescheduling is planned as a future enhancement. fileciteturn0file0L414-L423

## 🚀 Future Enhancements

### Progress Tracking

Allow students to record completed topics and update progress.

### Missed Session Detection

Detect missed sessions and automatically adjust the remaining schedule.

### Natural-Language Commands

Examples:

```text
"I have only 2 hours today."
```

```text
"Move DBMS revision to Saturday."
```

### Notifications

Add reminders for upcoming study sessions.

### Database Integration

Replace the JSON memory system with SQLite or another database.

### Performance Optimization

Use a smaller/faster local model for lower-end computers.

These enhancements are part of the provided project plan. fileciteturn0file0L426-L488

## 🎓 Learning Outcomes

The project covers:

- Artificial Intelligence
- AI agent concepts
- Python programming
- Streamlit development
- Local AI models
- Ollama
- Prompt engineering
- JSON-based data storage
- Environment configuration
- Persistent memory
- Interactive AI application design fileciteturn0file0L492-L506

## 🧪 Example

### Input

```text
Name: Anushka

Subjects:
DSA
Java
DBMS

Days remaining: 7
Available study hours: 3
```

### Output

```text
📚 Your Personalized Study Plan

DAY 1
DSA - Arrays - 1 hour
Java - OOP - 1 hour
DBMS - SQL - 1 hour

DAY 2
DSA - Searching - 1 hour
Java - Inheritance - 1 hour
DBMS - Normalization - 1 hour

DAY 3
DSA - Practice - 1 hour
Java - Exception Handling - 1 hour
DBMS - Practice Queries - 1 hour
```

The project documentation notes that the AI can also provide short exam-preparation tips. fileciteturn0file0L360-L389

## 👩‍💻 Author

**Anushka Sandip Dhumal**  
Department of Computer Science and Engineering  
Final Year  
Roll No.: 48  
Yashoda Technical Campus, Satara

## 👩‍🏫 Submitted To

**S.V. Balshetwar**  
Head of Department

## 📌 Conclusion

The AI Study Planner Agent demonstrates how Artificial Intelligence can be applied to a practical student problem. It accepts student information, analyzes study constraints, generates a personalized timetable, and stores the generated plan using persistent memory.

The project is designed to evolve into an agent that can remember progress, identify missed sessions, make decisions, and automatically modify the study plan. fileciteturn0file0L510-L518

---

**Project Title:** Development of an AI Study Planner Agent Using Python and Local AI
