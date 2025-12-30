import aiohttp
from config import TON_API_KEY, TON_WALLET, SUBSCRIPTION_PRICE, CHECK_LIMIT_TX

TON_API_URL = "https://tonapi.io/v2/blockchain/accounts"

async def find_valid_payment(telegram_id: int, used: dict):
    """
    Ищем входящий платёж:
    - value >= price
    - comment == INNER<telegram_id>
    - tx не использован ранее
    Возвращаем tx_hash или None
    """
    need_comment = f"INNER{telegram_id}"
    headers = {"Authorization": f"Bearer {TON_API_KEY}"}

    async with aiohttp.ClientSession(headers=headers) as session:
        url = f"{TON_API_URL}/{TON_WALLET}/transactions?limit={CHECK_LIMIT_TX}"
        async with session.get(url) as r:
            if r.status != 200:
                return None
            data = await r.json()

    for tx in data.get("transactions", []):
        tx_hash = tx.get("hash")
        if not tx_hash or tx_hash in used:
            continue

        in_msg = tx.get("in_msg")
        if not in_msg:
            continue

        value = int(in_msg.get("value", 0)) / 1e9
        comment = in_msg.get("message", "")

        if value >= SUBSCRIPTION_PRICE and comment == need_comment:
            return tx_hash

    return None