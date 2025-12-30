import os

def need(name: str):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"ENV {name} is missing")
    return value

BOT_TOKEN = need("BOT_TOKEN")
CHANNEL_LINK = need("CHANNEL_LINK")
TON_WALLET = need("TON_WALLET")
SUPPORT_USERNAME = need("SUPPORT_USERNAME")

SUBSCRIPTION_PRICE = float(need("SUBSCRIPTION_PRICE"))
SUBSCRIPTION_DAYS = int(need("SUBSCRIPTION_DAYS"))

TON_API_KEY = need("TON_API_KEY")