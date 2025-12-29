from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    text = (
        "🔥 INNER CIRCLE\n\n"
        "Ты зашёл не в обычный трейдинг-канал.\n\n"
        "Это закрытое пространство для тех, кто устал от шума, хаоса и азартных решений.\n\n"
        "Здесь — мышление, система и дисциплина."
    )
    await message.answer(text)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)