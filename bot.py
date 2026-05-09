from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import requests

TOKEN = "8645242729:AAELpQmB6-Kydw6lz6JJN11ScRUh5tAjeoQ"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# MENU
menu = ReplyKeyboardMarkup(resize_keyboard=True)
button1 = KeyboardButton("💵 Valyuta kursi")
menu.add(button1)

# START
@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    await message.answer(
        "✅ Menu ishladi",
        reply_markup=menu
    )

# VALYUTA
@dp.message_handler()
async def messages(message: types.Message):

    if message.text == "💵 Valyuta kursi":

        try:
            url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
            data = requests.get(url).json()

            usd = next(item for item in data if item["Ccy"] == "USD")
            eur = next(item for item in data if item["Ccy"] == "EUR")
            rub = next(item for item in data if item["Ccy"] == "RUB")

            text = f"""
💵 Valyuta kurslari

🇺🇸 USD: {usd['Rate']} so'm
🇪🇺 EUR: {eur['Rate']} so'm
🇷🇺 RUB: {rub['Rate']} so'm
"""

            await message.answer(text)

        except Exception as e:
            await message.answer(f"Xato: {e}")

# RUN
if __name__ == "__main__":
    print("Bot ishga tushdi")
    executor.start_polling(dp, skip_updates=True)
