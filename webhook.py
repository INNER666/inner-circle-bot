import os
import json
from aiohttp import web
from datetime import datetime, timedelta
from config import CHANNEL_LINK, SUBSCRIPTION_DAYS

def load_users():
    with open("data/users.json", "r") as f:
        return json.load(f)

def save_users(data):
    with open("data/users.json", "w") as f:
        json.dump(data, f, indent=2)

async def ton_webhook(request):
    data = await request.json()
    comment = data.get("comment")

    users = load_users()
    for uid, info in users.items():
        if info["code"] == comment:
            info["active"] = True
            info["expires"] = (datetime.utcnow() + timedelta(days=SUBSCRIPTION_DAYS)).isoformat()
            save_users(users)
            break

    return web.Response(text="ok")

app = web.Application()
app.router.add_post("/ton_webhook", ton_webhook)

PORT = int(os.getenv("PORT", 8080))
web.run_app(app, host="0.0.0.0", port=PORT)