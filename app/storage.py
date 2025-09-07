import os
import json

SUBMISSIONS_FILE = "data/submissions.json"
UPLOADS_FILE = "data/uploads.json"

def ensure_dirs() -> None:
    os.makedirs("images", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    os.makedirs("users", exist_ok=True)

def load_submissions():
    try:
        with open(SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_submissions(submissions) -> None:
    with open(SUBMISSIONS_FILE, "w", encoding="utf-8") as f:
        json.dump(submissions, f, ensure_ascii=False, indent=2)

def load_uploads():
    try:
        with open(UPLOADS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def save_uploads(uploads) -> None:
    with open(UPLOADS_FILE, "w", encoding="utf-8") as f:
        json.dump(uploads, f, ensure_ascii=False, indent=2)