import aiohttp
from config import TON_WALLET, SUBSCRIPTION_PRICE, TON_API_KEY

TON_API_URL = "https://tonapi.io/v2/blockchain/accounts"

async def check_payment(user_id: int) -> bool:
    comment = f"INNER_{user_id}"
    headers = {"Authorization": f"Bearer {TON_API_KEY}"}
    url = f"{TON_API_URL}/{TON_WALLET}/transactions?limit=20"

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                return False

            data = await resp.json()
            for tx in data.get("transactions", []):
                msg = tx.get("in_msg", {})
                value = int(msg.get("value", 0)) / 1e9
                text = msg.get("message", "")

                if value >= SUBSCRIPTION_PRICE and comment in text:
                    return True
    return False