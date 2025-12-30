import json
from datetime import datetime, timedelta

PAYMENTS_FILE = "data/payments.json"

def load():
    try:
        with open(PAYMENTS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save(data):
    with open(PAYMENTS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def mark_paid(user_id: str):
    data = load()
    until = (datetime.utcnow() + timedelta(days=30)).isoformat()
    data[user_id] = {"paid_until": until}
    save(data)
    return until