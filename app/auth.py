import json
import hashlib
from datetime import datetime

USERS_FILE = "users/users.json"

def hash_password(password: str) -> str:
    return hashlib.sha256(str.encode(password)).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hash_password(password) == hashed

def load_users() -> dict:
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_users(users: dict) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)

def register_user(username: str, password: str, region: str):
    from app.i18n import st, get_text  # lazily import to avoid circular
    users = load_users()
    if username in users:
        msg = "వినియోగదారు పేరు ఇప్పటికే ఉంది! 😅" if st.session_state.language == 'telugu' else "Username already exists! 😅"
        return False, msg
    users[username] = {
        "password": hash_password(password),
        "region": region,
        "created_at": datetime.now().isoformat(),
        "submissions": 0
    }
    save_users(users)
    msg = "నమోదు విజయవంతం! మా కమ్యూనిటీకి స్వాగతం! 🎉" if st.session_state.language == 'telugu' else "Registration successful! Welcome to our community! 🎉"
    return True, msg

def login_user(username: str, password: str):
    from app.i18n import st
    users = load_users()
    if username not in users:
        msg = "వినియోగదారు పేరు కనుగొనబడలేదు! 🤔" if st.session_state.language == 'telugu' else "Username not found! 🤔"
        return False, msg
    if verify_password(password, users[username]["password"]):
        msg = "ప్రవేశం విజయవంతం! తిరిగి స్వాగతం! 👋" if st.session_state.language == 'telugu' else "Login successful! Welcome back! 👋"
        return True, msg
    msg = "తప్పు పాస్‌వర్డ్! 🔐" if st.session_state.language == 'telugu' else "Incorrect password! 🔐"
    return False, msg