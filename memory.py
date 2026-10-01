"""Optional file-based memory utilities.

The current app uses Streamlit session state so old study plans and
checkboxes do not reappear after a browser refresh. These functions are
kept for compatibility with older project files.
"""

import json
from pathlib import Path

MEMORY_FILE = Path(__file__).resolve().parent / "study_memory.json"


def save_memory(data):
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def load_memory():
    if not MEMORY_FILE.exists():
        return {}

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, dict) else {}
    except (json.JSONDecodeError, OSError):
        return {}


def clear_memory():
    if MEMORY_FILE.exists():
        MEMORY_FILE.unlink()
