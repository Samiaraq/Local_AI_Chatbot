import json
import uuid
from pathlib import Path

SESSIONS_FOLDER= Path(__file__).parent/"sessions"
DEFAULT_TITLE="New Chat"
def ensure_sessions_folder():
    SESSIONS_FOLDER.mkdir(parents=True,exist_ok=True)

def generate_session_id():
    return str (uuid.uuid4())

#عشان يعطي الشات اسم 

DEFAULT_TITLE = "New Chat"
def make_title(first_message, max_length=40):
    title = first_message.strip()
    if not title:
        return DEFAULT_TITLE
    if len(title) > max_length:
        title = title[:max_length].rstrip() + "..."
    return title
def get_session_path(session_id):
    return SESSIONS_FOLDER /f"{session_id}.json"

def create_session():
    return {
        "session_id":generate_session_id(),
        "title":DEFAULT_TITLE,
        "messages":[]

    }
def save_session(session):
    ensure_sessions_folder()

    session_path = get_session_path(session["session_id"])

    with open(session_path, "w", encoding="utf-8") as file:
        json.dump(session, file, ensure_ascii=False, indent=2)

def load_session(session_id):
    session_path= get_session_path(session_id)
    if not session_path.exists():
        return None
    with open(session_path,"r",encoding="utf-8")as file:
        return json.load(file)
    
def add_message(session, role, content):
    session["messages"].append({
        "role": role,
        "content": content
    })
    if role == "user" and session["title"] == DEFAULT_TITLE:
        session["title"] = make_title(content)

def get_all_sessions():
    ensure_sessions_folder()
    sessions = []

    for file_path in SESSIONS_FOLDER.glob("*.json"):
        with open(file_path, "r", encoding="utf-8") as file:
            session = json.load(file)
            sessions.append(session)

    return sessions