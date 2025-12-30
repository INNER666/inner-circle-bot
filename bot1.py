import json
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from config import (
    BOT_TOKEN,
    CHANNEL_LINK,
    TON_WALLET,
    SUBSCRIPTION_PRICE,
    SUBSCRIPTION_DAYS,
    SUPPORT_USERNAME
)

from payments import mark_paid

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

USERS_FILE = "data/users.json"


# ---------- utils ----------
def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open(USERS_FILE, "w") as f:
        json.dump(data, f, indent=2)


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
    kb.add(
        types.InlineKeyboardButton("🔄 Я оплатил", callback_data="check"),
        types.InlineKeyboardButton("⬅️ Назад", callback_data="back"),
    )
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
    await m.answer(text, reply_markup=main_kb(), parse_mode="Markdown")


# ---------- sections ----------
@dp.callback_query_handler(lambda c: c.data == "about")
async def about(c: types.CallbackQuery):
    text = (
        "🔥 *INNER CIRCLE*\n\n"
        "Это не сигнальный канал.\n"
        "Это система мышления и дисциплины.\n\n"
        "Мы не обещаем прибыль.\n"
        "Мы учим думать и принимать решения."
    )
    await c.message.edit_text(text, reply_markup=back_kb(), parse_mode="Markdown")


@dp.callback_query_handler(lambda c: c.data == "inside")
async def inside(c: types.CallbackQuery):
    text = (
        "📊 *Что внутри:*\n\n"
        "• Аналитика рынка\n"
        "• Разборы сделок\n"
        "• Работа с рисками\n"
        "• Психология трейдинга\n"
        "• Системное мышление"
    )
    await c.message.edit_text(text, reply_markup=back_kb(), parse_mode="Markdown")


@dp.callback_query_handler(lambda c: c.data == "price")
async def price(c: types.CallbackQuery):
    text = (
        "💰 *Подписка INNER CIRCLE*\n\n"
        f"Цена: *{SUBSCRIPTION_PRICE} TON*\n"
        f"Срок: *{SUBSCRIPTION_DAYS} дней*\n\n"
        "Оплата через TON.\n"
        "После оплаты нажми кнопку ниже."
    )
    await c.message.edit_text(text, reply_markup=pay_kb(), parse_mode="Markdown")


@dp.callback_query_handler(lambda c: c.data == "support")
async def support(c: types.CallbackQuery):
    await c.message.edit_text(
        f"🆘 Поддержка:\n\n👉 @{SUPPORT_USERNAME}",
        reply_markup=back_kb()
    )


@dp.callback_query_handler(lambda c: c.data == "back")
async def back(c: types.CallbackQuery):
    await start(c.message)


# ---------- payment ----------
@dp.callback_query_handler(lambda c: c.data == "check")
async def check_payment(c: types.CallbackQuery):
    user_id = str(c.from_user.id)

    until = mark_paid(user_id)

    users = load_users()
    users[user_id] = {
        "active": True,
        "paid_until": until
    }
    save_users(users)

    await c.message.edit_text(
        "✅ *Подписка активирована!*\n\n"
        f"Доступ до: `{until}`\n\n"
        f"🔗 Канал: {CHANNEL_LINK}",
        reply_markup=renew_kb(),
        parse_mode="Markdown"
    )


@dp.callback_query_handler(lambda c: c.data == "pay")
async def pay(c: types.CallbackQuery):
    text = (
        "💳 *Оплата подписки*\n\n"
        f"Сумма: *{SUBSCRIPTION_PRICE} TON*\n"
        f"Кошелёк:\n`{TON_WALLET}`\n\n"
        f"📝 Комментарий к платежу:\n`{c.from_user.id}`"
    )
    await c.message.edit_text(text, reply_markup=pay_kb(), parse_mode="Markdown")


# ---------- run ----------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)