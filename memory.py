import json
from pathlib import Path


MEMORY_FILE = Path(__file__).resolve().parent / "study_memory.json"


def save_memory(data):
    """Save the student's study information."""

    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False
        )


def load_memory():
    """Load saved study information."""

    if not MEMORY_FILE.exists():
        return {}

    with open(MEMORY_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def clear_memory():
    """Delete saved study information."""

    if MEMORY_FILE.exists():
        MEMORY_FILE.unlink()