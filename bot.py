from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import requests

TOKEN = "8645242729:AAELpQmB6-Kydw6lz6JJN11ScRUh5tAjeoQ"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add(KeyboardButton("💵 Valyuta kursi"))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "✅ Bot ishladi",
        reply_markup=menu
    )

@dp.message_handler()
async def handler(message: types.Message):

    if message.text == "💵 Valyuta kursi":

        url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        data = requests.get(url).json()

        usd = next(x for x in data if x["Ccy"] == "USD")
        eur = next(x for x in data if x["Ccy"] == "EUR")
        rub = next(x for x in data if x["Ccy"] == "RUB")

        text = f"""
💵 Valyuta kurslari

🇺🇸 USD: {usd['Rate']} so'm
🇪🇺 EUR: {eur['Rate']} so'm
🇷🇺 RUB: {rub['Rate']} so'm
"""

        await message.answer(text)

if __name__ == "__main__":
    print("Bot ishga tushdi")
    executor.start_polling(dp, skip_updates=True)
