from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
import asyncio

TOKEN = "8645242729:AAELpQmB6-Kydw6lz6JJN11ScRUh5tAjeoQ"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: types.Message):
    await message.answer(
        "✅ Assalomu alaykum!\n\n@Analyticuz_bot ishga tushdi."
    )

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
