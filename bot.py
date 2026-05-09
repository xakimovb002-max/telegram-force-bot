from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
import requests

TOKEN = "8645242729:AAELpQmB6-Kydw6lz6JJN11ScRUh5tAjeoQ"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# MENU
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add("💵 Valyuta kursi")

# START
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer(
        "✅ Menu ishladi",
        reply_markup=menu
    )

# VALYUTA
@dp.message_handler(lambda message: message.text == "💵 Valyuta kursi")
async def valyuta(message: types.Message):
    try:
        url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        response = requests.get(url).json()

        usd = next((x for x in response if x["Ccy"] == "USD"), None)
        eur = next((x for x in response if x["Ccy"] == "EUR"), None)
        rub = next((x for x in response if x["Ccy"] == "RUB"), None)

        text = f"""
💵 Valyuta kurslari:

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
