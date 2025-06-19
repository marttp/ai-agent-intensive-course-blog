import os
import json
from genai_client import client

HISTORY_FILE = "chat_history.json"

def load_history():
    """Load chat history from file if it exists"""
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, 'r') as f:
                history_data = json.load(f)
                print(f"Loaded {len(history_data)} previous messages")
                return history_data
        except (json.JSONDecodeError, IOError):
            print("Warning: Could not load history file, starting fresh")
    return []

def save_history(chat):
    """Save chat history to file"""
    try:
        history_data = []
        for message in chat.get_history():
            history_data.append({
                "role": message.role,
                "parts": [{"text": part.text} for part in message.parts if hasattr(part, 'text') and part.text]
            })
        
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history_data, f, indent=2)
        print(f"History saved to {HISTORY_FILE}")
    except Exception as e:
        print(f"Warning: Could not save history: {e}")

# Load existing history
history = load_history()

# Create chat with loaded history to revive conversation
chat = client.chats.create(model="gemini-2.0-flash", history=history)

response = chat.send_message("Where were we?")
print(response.text)