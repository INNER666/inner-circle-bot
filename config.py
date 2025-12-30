import os

# Telegram
BOT_TOKEN = os.getenv("BOT_TOKEN")

# TON
TON_API_KEY = os.getenv("TON_API_KEY")
TON_WALLET = "UQB5B1BKxlB1ewLXCDlI67bT3kby30FSIvmHDbFz9ZmwujFT"

# Project
CHANNEL_LINK = "https://t.me/+mVhziBGQFTlhY2Uy"
SUPPORT_USERNAME = "@Phoenix_00000000"

# Subscription
SUBSCRIPTION_PRICE = 3        # TON
SUBSCRIPTION_DAYS = 30

# Behavior
CHECK_LIMIT_TX = 25           # how many tx to scan
REMIND_DAYS = (7, 3, 1)       # reminders before expiry