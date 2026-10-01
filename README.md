🤖 AI Study Planner Agent
An intelligent, multi-module exam preparation assistant built with Streamlit and powered by Groq Cloud AI (openai/gpt-oss-20b). The application designs customized daily study timetables, tracks real-time progress across multiple subjects, intelligently reschedules missed sessions without overloading daily study limits, and provides an interactive AI study tutor.

📑 Table of Contents
Overview
Key Features
Module 1: AI Study Plan Generator
Module 2: Automatic Study Progress Tracker
Module 3: AI Missed Session Rescheduler
Module 4: AI Study Assistant
Project Architecture
Directory Structure
Getting Started
Prerequisites
Installation
Environment Configuration
Running the App
Usage Guide
Technologies Used
License
🌟 Overview
Preparing for exams across multiple subjects can quickly become overwhelming, especially when unexpected delays or missed study sessions occur.

The AI Study Planner Agent solves this by:

Creating an optimal, realistic timetable distributed across available daily study hours.
Tracking granular session completion day-by-day.
Automatically redistributing missed topics across remaining days with dedicated catch-up strategies.
Answering questions and clarifying concepts directly through an integrated AI Study Assistant.
🚀 Key Features
📅 Module 1: AI Study Plan Generator
Generates a day-by-day structured timetable tailored to:
Student Name
Subjects List (e.g., DSA, Java, DBMS, Mathematics)
Days Remaining until exam
Available Study Hours per day
Integrates dedicated revision intervals, practice problem blocks, mock tests near the exam, and actionable exam tips.
Displays the generated plan cleanly without auto-scrolling or viewport jumping.
📊 Module 2: Automatic Study Progress Tracker
Automatically dynamically populates interactive checkboxes for every subject and every day.
Computes both:
Overall Completion Percentage across all sessions.
Subject-wise Progress Bars and statistics (e.g., Java: 75.0% (3/4 sessions)).
Automatically syncs progress state to persistent storage.
🔄 Module 3: AI Missed Session Rescheduler
Accommodates both Single Session missed (1 day / 1 topic) and Multiple Days Backlog (absence of more than 1 day).
Intelligently redistributes missed topics across remaining days without exceeding maximum daily study hours.
Displays a clean, targeted 3-section output:
### 🔄 Rescheduled Days: Lists affected days, subjects, and hours added/shifted.
### ➕ Added / Shifted Plan: Explicitly maps affected sessions (- Day X → Subject – Topic — duration).
### 💡 Reason: Concise explanation of the redistribution strategy.
Automatically preserves and updates the active master schedule in memory for the assistant.
💬 Module 4: AI Study Assistant
Context-aware chatbot with complete visibility into:
Student profile and available study hours
Original study timetable
Active rescheduled plan (if modified)
Current completion percentage and completed sessions
Last reported missed sessions
Offers personalized study guidance, concept clarification, and schedule advice.
Includes quick-action Clear Chat button to reset conversations at any time.
⚙️ Sidebar Controls & Persistence
Displays active student profile and timetable status (Original Plan Active 📚 or Rescheduled Plan Active ⚡).
Reset & Start Fresh: One-click wipe of all cached plans, session states, and disk memory.
File-backed persistence via study_memory.json ensures state is safely preserved across browser sessions.
🏗️ Project Architecture

                      +-----------------------------+
                      |       Streamlit Web UI      |
                      |          (app.py)           |
                      +--------------+--------------+
                                     |
             +-----------------------+-----------------------+
             |                                               |
             v                                               v
+--------------------------+                   +--------------------------+
|       AI Agent Core      |                   |     Persistent Memory    |
|        (agent.py)        |                   |       (memory.py)        |
+------------+-------------+                   +------------+-------------+
             |                                               |
             v                                               v
+--------------------------+                   +--------------------------+
|      Groq Cloud API      |                   |    study_memory.json     |
|   (openai/gpt-oss-20b)   |                   |  (Profile, Plan, State)  |
+--------------------------+                   +--------------------------+
📂 Directory Structure
text

HOD_Activity/
│
├── app.py                 # Streamlit frontend & application orchestration
├── agent.py               # Groq AI agent logic (generation, rescheduling, assistant)
├── memory.py              # File-based JSON persistence utilities
├── study_memory.json      # Persistent local storage for user plan & progress (auto-created)
├── requirements.txt       # Project Python dependencies
├── .env                   # Environment secrets (GROQ_API_KEY)
└── README.md              # Project documentation
🛠️ Getting Started
Prerequisites
Python 3.10+ installed on your system.
A Groq API Key (get one free at console.groq.com).
Installation
Navigate to the Project Directory:

bash

cd path/to/HOD_Activity
Create and Activate a Virtual Environment:

Windows:
powershell

python -m venv venv
.\venv\Scripts\activate
macOS / Linux:
bash

python3 -m venv venv
source venv/bin/activate
Install Dependencies:

bash

pip install -r requirements.txt
Environment Configuration
Create a .env file in the root directory:

env

GROQ_API_KEY=gsk_your_actual_groq_api_key_here
Running the App
Launch the Streamlit web server:

bash

streamlit run app.py
The application will start and open automatically in your browser at:

http://localhost:8501
📖 Usage Guide
Generate Your Timetable (Module 1):

Enter your name, list of subjects (one per line), total days remaining, and study hours available per day.
Click 🚀 Generate My Study Plan.
Your personalized plan is rendered immediately below without shifting your viewport.
Track Daily Sessions (Module 2):

As you finish daily study blocks, check the corresponding checkboxes under Complete Your Study Sessions.
Watch your overall progress and subject breakdown progress bars update in real time.
Handle Missed Sessions (Module 3):

If an unexpected emergency occurs, select whether you missed a single session or multiple days.
Specify the missed day(s), subject, and topic.
Click 🔄 Reschedule With AI.
View the targeted Rescheduled Days, Added / Shifted Plan, and Reason.
Ask the AI Study Assistant (Module 4):

Type questions like "What should I focus on today?" or "Explain how my missed Java topic was redistributed."
Receive contextual advice based on your current study schedule and completed sessions.
💻 Technologies Used
Technology	Purpose
Python	Core backend language
Streamlit	Interactive reactive web UI framework
Groq API	Ultra-fast LLM inference
openai/gpt-oss-20b	LLM model for planning, rescheduling, and conversational tutoring
python-dotenv	Secure environment variable configuration
