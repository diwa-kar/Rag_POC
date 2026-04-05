from collections import defaultdict

# In-memory store (good enough for assignment)
chat_store = defaultdict(list)


def add_message(session_id, role, content):
    chat_store[session_id].append({
        "role": role,
        "content": content
    })


def get_history(session_id, max_turns=5):
    history = chat_store[session_id][-max_turns:]
    return history