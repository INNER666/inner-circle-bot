import os

def need(name: str):
    v = os.getenv(name)
    if not v:
        raise RuntimeError(f"ENV {name} is missing")
    return v

BOT_TOKEN = need("BOT_TOKEN")
CHANNEL_LINK = need("CHANNEL_LINK")
TON_WALLET = need("TON_WALLET")

SUBSCRIPTION_PRICE = float(need("SUBSCRIPTION_PRICE"))
SUBSCRIPTION_DAYS = int(need("SUBSCRIPTION_DAYS"))

SUPPORT_USERNAME = need("SUPPORT_USERNAME")