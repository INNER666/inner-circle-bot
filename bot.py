import json
import uuid
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import BOT_TOKEN, CHANNEL_LINK, TON_WALLET, SUBSCRIPTION_PRICE

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

def load_users():
    try:
        with open("data/users.json", "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open("data/users.json", "w") as f:
        json.dump(data, f, indent=2)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    text = (
        "🔒 *INNER CIRCLE*\n\n"
        "Ты зашёл не в обычный трейдинг-канал.\n\n"
        "Это закрытое пространство для тех, кто устал от шума, "
        "хаоса и азартных решений.\n\n"
        "Здесь — мышление, система и дисциплина."
    )
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Продолжить", callback_data="next"))
    await message.answer(text, parse_mode="Markdown", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "next")
async def next_step(call):
    text = (
        "⚠️ *Важно понять*\n\n"
        "Если ты ищешь лёгкие деньги — это не для тебя.\n\n"
        "Если ты готов думать и соблюдать риск — ты по адресу."
    )
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Я понимаю", callback_data="price"))
    await call.message.edit_text(text, parse_mode="Markdown", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "price")
async def price(call):
    text = (
        f"💎 *Доступ в INNER CIRCLE*\n\n"
        f"Формат: ежемесячная подписка\n\n"
        f"🔥 Цена: *{SUBSCRIPTION_PRICE} TON / месяц*\n\n"
        "Оплата = доступ в закрытый канал."
    )
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Получить доступ", callback_data="pay"))
    await call.message.edit_text(text, parse_mode="Markdown", reply_markup=kb)

@dp.callback_query_handler(lambda c: c.data == "pay")
async def pay(call):
    users = load_users()
    code = str(uuid.uuid4())[:8]

    users[str(call.from_user.id)] = {
        "code": code,
        "active": False
    }
    save_users(users)

    text = (
        f"💳 *Оплата доступа*\n\n"
        f"Переведи *{SUBSCRIPTION_PRICE} TON* на адрес:\n"
        f"{TON_WALLET}\n\n"
        f"📝 *Комментарий к платежу:*\n"
        f"{code}\n\n"
        "После подтверждения доступ откроется автоматически."
    )
    await call.message.edit_text(text, parse_mode="Markdown")

if name == "main":
    executor.start_polling(dp)