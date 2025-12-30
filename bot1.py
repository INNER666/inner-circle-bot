import json
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

from config import (
    BOT_TOKEN, CHANNEL_LINK, TON_WALLET,
    SUBSCRIPTION_PRICE, SUBSCRIPTION_DAYS,
    SUPPORT_USERNAME
)
from payments import check_payment

bot = Bot(token=BOT_TOKEN, parse_mode="Markdown")
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
        types.InlineKeyboardButton("💰 Условия и оплата", callback_data="pay"),
        types.InlineKeyboardButton("🆘 Поддержка", callback_data="support"),
    )
    return kb

def back_kb():
    return types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("⬅️ Назад", callback_data="back")
    )

def pay_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🔄 Я оплатил", callback_data="check"))
    kb.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    return kb


# ---------- start ----------
@dp.message_handler(commands=["start"])
async def start(m: types.Message):
    users = load_users()
    uid = str(m.from_user.id)

    if uid not in users:
        users[uid] = {"active": False, "expires": None}
        save_users(users)

    text = (
        "🔥 *INNER CIRCLE*\n\n"
        "Ты зашёл не в обычный трейдинг-канал.\n\n"
        "Это закрытое пространство для тех, кто устал от шума,\n"
        "хаоса и азартных решений.\n\n"
        "*Здесь — мышление, система и дисциплина.*"
    )
    await m.answer(text, reply_markup=main_kb())


# ---------- callbacks ----------
@dp.callback_query_handler(lambda c: c.data == "about")
async def about(c: types.CallbackQuery):
    await c.message.edit_text(
        "INNER CIRCLE — это не сигналы.\n"
        "Это мышление, риск-менеджмент и системный подход.\n\n"
        "Мы не обещаем 100%.\n"
        "Мы учим принимать *правильные решения*.",
        reply_markup=back_kb()
    )

@dp.callback_query_handler(lambda c: c.data == "inside")
async def inside(c: types.CallbackQuery):
    await c.message.edit_text(
        "📊 *Что внутри:*\n\n"
        "• Аналитика\n"
        "• Логика входов\n"
        "• Контроль риска\n"
        "• Работа с психологией\n"
        "• Реальные кейсы",
        reply_markup=back_kb()
    )

@dp.callback_query_handler(lambda c: c.data == "pay")
async def pay(c: types.CallbackQuery):
    uid = c.from_user.id
    await c.message.edit_text(
        f"💰 *Условия доступа*\n\n"
        f"Цена: *{SUBSCRIPTION_PRICE} TON*\n"
        f"Срок: *{SUBSCRIPTION_DAYS} дней*\n\n"
        f"Кошелёк:\n`{TON_WALLET}`\n\n"
        f"Комментарий:\n`INNER_{uid}`",
        reply_markup=pay_kb()
    )

@dp.callback_query_handler(lambda c: c.data == "check")
async def check(c: types.CallbackQuery):
    uid = c.from_user.id
    users = load_users()

    await c.answer("🔎 Проверяю платёж...")

    if await check_payment(uid):
        users[str(uid)]["active"] = True
        users[str(uid)]["expires"] = (
            datetime.utcnow() + timedelta(days=SUBSCRIPTION_DAYS)
        ).isoformat()
        save_users(users)

        await c.message.edit_text(
            f"✅ *Платёж подтверждён!*\n\n"
            f"Доступ:\n{CHANNEL_LINK}"
        )
    else:
        await c.answer(
            "❌ Платёж не найден.\n"
            "Проверь сумму и комментарий.",
            show_alert=True
        )

@dp.callback_query_handler(lambda c: c.data == "support")
async def support(c: types.CallbackQuery):
    await c.message.edit_text(
        f"🆘 Поддержка:\n@{SUPPORT_USERNAME}",
        reply_markup=back_kb()
    )

@dp.callback_query_handler(lambda c: c.data == "back")
async def back(c: types.CallbackQuery):
    await start(c.message)


# ---------- run ----------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)