from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import requests

TOKEN = "8645242729:AAELpQmB6-Kydw6lz6JJN11ScRUh5tAjeoQ"

OPENWEATHER_API = "fb5b0254527ec050c0e71ece00768863"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

menu = ReplyKeyboardMarkup(resize_keyboard=True)

menu.add(
    KeyboardButton("🌦 Ob-havo"),
    KeyboardButton("💵 Valyuta kursi")
)

menu.add(
    KeyboardButton("👥 Referral sistema"),
    KeyboardButton("📊 Statistika")
)

menu.add(
    KeyboardButton("📢 Reklama yuborish"),
    KeyboardButton("🔐 Majburiy obuna")
)

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("✅ Menu ishladi", reply_markup=menu)

@dp.message_handler(lambda message: message.text == "💵 Valyuta kursi")
async def valyuta(message: types.Message):
    try:
        url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        data = requests.get(url).json()

        usd = data[0]['Rate']
        eur = data[1]['Rate']
        rub = data[2]['Rate']

        text = f"""
💵 Valyuta kurslari

🇺🇸 USD: {usd} so'm
🇪🇺 EUR: {eur} so'm
🇷🇺 RUB: {rub} so'm
"""

        await message.answer(text)

    except Exception as e:
        await message.answer(f"Xatolik: {e}")

@dp.message_handler(lambda message: message.text == "🌦 Ob-havo")
async def ob_havo(message: types.Message):
    try:
        city = "Tashkent"

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API}&units=metric"

        data = requests.get(url).json()

        temp = data['main']['temp']
        desc = data['weather'][0]['description']

        text = f"""
🌦 Tashkent ob-havo

🌡 Harorat: {temp}°C
☁️ Holat: {desc}
"""

        await message.answer(text)

    except Exception as e:
        await message.answer(f"Xatolik: {e}")

print("Bot ishga tushdi")

executor.start_polling(dp, skip_updates=True)
