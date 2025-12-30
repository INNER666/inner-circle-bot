import json, asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from config import (
    BOT_TOKEN, CHANNEL_LINK, TON_WALLET,
    SUBSCRIPTION_PRICE, SUBSCRIPTION_DAYS,
    SUPPORT_USERNAME, REMIND_DAYS
)
from payments import find_valid_payment

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

USERS = "data/users.json"
PAYMENTS = "data/payments.json"

# ---------- utils ----------
def jload(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        return {}

def jsave(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def now():
    return datetime.utcnow()

def extend_until(current_until_iso: str | None):
    base = now()
    if current_until_iso:
        try:
            cur = datetime.fromisoformat(current_until_iso)
            if cur > base:
                base = cur
        except:
            pass
    return (base + timedelta(days=SUBSCRIPTION_DAYS)).isoformat()

# ---------- keyboards ----------
def main_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("🔥 Что такое INNER CIRCLE", callback_data="about"),
        types.InlineKeyboardButton("📊 Что внутри", callback_data="inside"),
        types.InlineKeyboardButton("💰 Условия и оплата", callback_data="price"),
        types.InlineKeyboardButton("🆘 Поддержка", callback_data="support"),
    )
    return kb

def back_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    return kb

def pay_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔄 Я оплатил", callback_data="check"))
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    return kb

def renew_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔁 Продлить подписку", callback_data="pay"))
    return kb

# ---------- start ----------
@dp.message_handler(commands=["start"])
async def start(m: types.Message):
    text = (
        "🔥 *INNER CIRCLE*\n\n"
        "Ты зашёл не в обычный трейдинг-канал.\n\n"
        "Это закрытое пространство для тех, кто устал от шума, хаоса и азартных решений.\n\n"
        "Здесь — мышление, система и дисциплина."
    )
    await m.answer(text, parse_mode="Markdown", reply_markup=main_kb())

# ---------- pages ----------
@dp.callback_query_handler(lambda c: c.data == "about")
async def about(c: types.CallbackQuery):
    await c.message.edit_text(
        "INNER CIRCLE — не казино и не «гарантии».\n\n"
        "Мы не обещаем доход.\n"
        "Мы даём систему, мышление и инструменты.\n\n"
        "Решения — твои. Ответственность — твоя.",
        reply_markup=back_kb()
    )

@dp.callback_query_handler(lambda c: c.data == "inside")
async def inside(c: types.CallbackQuery):
    await c.message.edit_text(
        "📊 *Внутри клуба:*\n\n"
        "• Торговые идеи и сценарии\n"
        "• Логика входа/выхода\n"
        "• Риск-менеджмент\n"
        "• Психология\n"
        "• Ошибки рынка\n"
        "• Мышление сильных",
        parse_mode="Markdown",
        reply_markup=back_kb()
    )

@dp.callback_query_handler(lambda c: c.data == "price")
async def price(c: types.CallbackQuery):
    await c.message.edit_text(
        f"💰 *Условия доступа*\n\n"
        f"• Цена: *{SUBSCRIPTION_PRICE} TON*\n"
        f"• Срок: *{SUBSCRIPTION_DAYS} дней*\n"
        "• Первые 100 участников\n\n"
        "❗ Не финсовет. Мы обучаем, не гарантируем результат.",
        parse_mode="Markdown",
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("✅ Получить доступ", callback_data="pay"),
            types.InlineKeyboardButton("⬅️ Назад", callback_data="back")
        )
    )

# ---------- pay ----------
@dp.callback_query_handler(lambda c: c.data == "pay")
async def pay(c: types.CallbackQuery):
    tg = c.from_user.id
    await c.message.edit_text(
        "💳 *Оплата доступа*\n\n"
        f"Сумма: *{SUBSCRIPTION_PRICE} TON*\n"
        f"Кошелёк:\n`{TON_WALLET}`\n\n"
        "📝 *Комментарий (обязательно):*\n"
        f"`INNER{tg}`\n\n"
        "После оплаты нажми кнопку ниже.",
        parse_mode="Markdown",
        reply_markup=pay_kb()
    )

# ---------- check payment ----------
@dp.callback_query_handler(lambda c: c.data == "check")
async def check(c: types.CallbackQuery):
    uid = str(c.from_user.id)
    users = jload(USERS)
    pays = jload(PAYMENTS)

    # активная подписка?
    if uid in users:
        try:
            if datetime.fromisoformat(users[uid]["until"]) > now():
                await c.answer("У тебя уже есть активный доступ.", show_alert=True)
                return
        except:
            pass

    tx = await find_valid_payment(int(uid), pays)
    if not tx:
        await c.answer("Платёж не найден. Проверь сумму и комментарий.", show_alert=True)
        return

    # зафиксировать платёж
    pays[tx] = {"user": uid, "at": now().isoformat()}
    jsave(PAYMENTS, pays)

    # продлить/активировать
    new_until = extend_until(users.get(uid, {}).get("until"))
    users[uid] = {"until": new_until}
    jsave(USERS, users)

    await c.message.edit_text(
        "✅ *Оплата подтверждена!*\n\n"
        f"Вход в закрытый канал:\n{CHANNEL_LINK}",
        parse_mode="Markdown"
    )

# ---------- support ----------
@dp.callback_query_handler(lambda c: c.data == "support")
async def support(c: types.CallbackQuery):
    await c.message.edit_text(
        f"🆘 Поддержка:\n\n{SUPPORT_USERNAME}",
        reply_markup=back_kb()
    )

@dp.callback_query_handler(lambda c: c.data == "back")
async def back(c: types.CallbackQuery):
    await start(c.message)

# ---------- background tasks ----------
async def reminders_loop():
    while True:
        users = jload(USERS)
        for uid, data in users.items():
            try:
                until = datetime.fromisoformat(data["until"])
                days = (until - now()).days
                if days in REMIND_DAYS:
                    try:
                        await bot.send_message(
                            uid,
                            f"⏳ Подписка заканчивается через {days} дн.\n"
                            "Чтобы сохранить доступ — продли подписку.",
                            reply_markup=renew_kb()
                        )
                    except:
                        pass
                if days < 0:
                    # истекла — уведомим
                    try:
                        await bot.send_message(
                            uid,
                            "⛔️ Подписка истекла.\n"
                            "Доступ остановлен. Продли, чтобы вернуться.",
                            reply_markup=renew_kb()
                        )
                    except:
                        pass
            except:
                pass
        await asyncio.sleep(86400)

async def on_startup(dp):
    asyncio.create_task(reminders_loop())

# ---------- run ----------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)