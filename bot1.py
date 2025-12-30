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

from payments import check_payment


# ---------------- INIT ----------------
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

USERS_FILE = "data/users.json"


# ---------------- STORAGE ----------------
def load_users():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}

def save_users(data):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# ---------------- KEYBOARDS ----------------
def next_kb(step):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Дальше →", callback_data=f"intro_{step}"))
    return kb

def menu_kb():
    kb = types.InlineKeyboardMarkup(row_width=1)
    kb.add(
        types.InlineKeyboardButton("🔥 Что такое INNER CIRCLE", callback_data="about"),
        types.InlineKeyboardButton("📊 Что внутри", callback_data="inside"),
        types.InlineKeyboardButton("💰 Условия и оплата", callback_data="pay"),
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

def channel_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📢 Перейти в канал", url=CHANNEL_LINK))
    return kb


# ---------------- INTRO TEXTS ----------------
INTRO_1 = (
    "🔥 INNER CIRCLE\n\n"
    "Ты зашёл не в обычный трейдинг-канал.\n\n"
    "Это закрытое пространство для людей, которые понимают риск "
    "и хотят выстроить системный подход, а не надеяться на удачу."
)

INTRO_2 = (
    "INNER CIRCLE — это не про быстрые деньги.\n\n"
    "Это про мышление, дисциплину и принятие решений "
    "в условиях неопределённости.\n\n"
    "Мы работаем на дистанции, а не на эмоциях."
)

INTRO_3 = (
    "Здесь нет обещаний прибыли.\n"
    "Здесь нет 100% сигналов.\n\n"
    "Каждый участник сам несёт ответственность "
    "за управление своим капиталом.\n\n"
    "Наша задача — дать структуру и логику."
)

INTRO_4 = (
    "Если ты устал от хаоса и импульсивных сделок —\n"
    "ты по адресу.\n\n"
    "Если ты ищешь лёгкие деньги —\n"
    "этот проект не для тебя."
)


# ---------------- HANDLERS ----------------
@dp.message_handler(commands=["start"])
async def start(m: types.Message):
    users = load_users()
    uid = str(m.from_user.id)

    if uid not in users:
        users[uid] = {
            "active": False,
            "expires": None,
            "joined": datetime.utcnow().isoformat()
        }
        save_users(users)

    await m.answer(INTRO_1, reply_markup=next_kb(2))


@dp.callback_query_handler(text="intro_2")
async def intro_2(c: types.CallbackQuery):
    await c.message.edit_text(INTRO_2, reply_markup=next_kb(3))
    await c.answer()

@dp.callback_query_handler(text="intro_3")
async def intro_3(c: types.CallbackQuery):
    await c.message.edit_text(INTRO_3, reply_markup=next_kb(4))
    await c.answer()

@dp.callback_query_handler(text="intro_4")
async def intro_4(c: types.CallbackQuery):
    await c.message.edit_text(INTRO_4, reply_markup=menu_kb())
    await c.answer()


@dp.callback_query_handler(text="about")
async def about(c: types.CallbackQuery):
    await c.message.edit_text(
        "🔥 Что такое INNER CIRCLE\n\n"
        "Это система мышления и дисциплины.\n"
        "Мы не продаём сигналы ради сигналов.\n\n"
        "Мы учим понимать рынок и управлять риском.",
        reply_markup=back_kb()
    )
    await c.answer()


@dp.callback_query_handler(text="inside")
async def inside(c: types.CallbackQuery):
    await c.message.edit_text(
        "📊 Что внутри\n\n"
        "• Аналитика рынка\n"
        "• Логика входов и выходов\n"
        "• Риск-менеджмент\n"
        "• Психология трейдера\n"
        "• Работа над дисциплиной",
        reply_markup=back_kb()
    )
    await c.answer()


@dp.callback_query_handler(text="pay")
async def pay(c: types.CallbackQuery):
    await c.message.edit_text(
        f"💰 Условия доступа\n\n"
        f"Стоимость: {SUBSCRIPTION_PRICE} TON\n"
        f"Срок: {SUBSCRIPTION_DAYS} дней\n\n"
        f"Кошелёк:\n{TON_WALLET}\n\n"
        f"Комментарий:\nINNER_{c.from_user.id}\n\n"
        "После оплаты нажми кнопку ниже.",
        reply_markup=pay_kb()
    )
    await c.answer()


@dp.callback_query_handler(text="check")
async def check(c: types.CallbackQuery):
    users = load_users()
    uid = str(c.from_user.id)

    await c.answer("Проверяю платёж...")

    if await check_payment(c.from_user.id):
        users[uid]["active"] = True
        users[uid]["expires"] = (
            datetime.utcnow() + timedelta(days=SUBSCRIPTION_DAYS)
        ).isoformat()
        save_users(users)

        await c.message.edit_text(
            "✅ Оплата подтверждена.\n\n"
            "Добро пожаловать в INNER CIRCLE.\n"
            "Доступ в канал по кнопке ниже.",
            reply_markup=channel_kb()
        )
    else:
        await c.answer(
            "Платёж не найден.\n"
            "Проверь сумму и комментарий.",
            show_alert=True
        )


@dp.callback_query_handler(text="support")
async def support(c: types.CallbackQuery):
    await c.message.edit_text(
        "🆘 Поддержка\n\n"
        "По вопросам доступа и оплаты напиши напрямую:\n\n"
        f"@{SUPPORT_USERNAME}",
        reply_markup=back_kb()
    )
    await c.answer()


@dp.callback_query_handler(text="back")
async def back(c: types.CallbackQuery):
    await c.message.edit_text(INTRO_4, reply_markup=menu_kb())
    await c.answer()


# ---------------- RUN ----------------
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)