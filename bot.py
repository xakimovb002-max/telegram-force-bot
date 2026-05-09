from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
import requests

TOKEN = "8645242729:AAELpQmB6-Kydw6lz6JJN11ScRUh5tAjeoQ"
WEATHER_API = "fb5b0254527ec050c0e71ece00768863"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# MENU
menu = ReplyKeyboardMarkup(resize_keyboard=True)

menu.add(
    KeyboardButton("👥 Referral sistema"),
    KeyboardButton("📊 Statistika")
)

menu.add(
    KeyboardButton("🌦 Ob-havo"),
    KeyboardButton("💵 Valyuta kursi")
)

menu.add(
    KeyboardButton("📢 Reklama yuborish")
)

menu.add(
    KeyboardButton("🔐 Majburiy obuna")
)

# START
@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(
        "✅ Menu ishladi",
        reply_markup=menu
    )

# OB-HAVO
@dp.message_handler(lambda message: message.text == "🌦 Ob-havo")
async def weather(message: types.Message):

    city = "Tashkent"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric"

    data = requests.get(url).json()

    temp = data["main"]["temp"]
    desc = data["weather"][0]["description"]

    await message.answer(
        f"🌦 Shahar: {city}\n"
        f"🌡 Harorat: {temp}°C\n"
        f"☁️ Holat: {desc}"
    )

# VALYUTA
@dp.message_handler(lambda message: message.text == "💵 Valyuta kursi")
async def kurs(message: types.Message):

    url = "https://cbu.uz/uz/arkhiv-kursov-valyut/json/USD/"
    data = requests.get(url).json()

    price = data[0]["Rate"]

    await message.answer(
        f"💵 1 USD = {price} so'm"
    )

# REFERAL
@dp.message_handler(lambda message: message.text == "👥 Referral sistema")
async def referal(message: types.Message):

    link = f"https://t.me/Analytic?start={message.from_user.id}"

    await message.answer(
        f"👥 Sizning referal linkingiz:\n{link}"
    )

# STATISTIKA
@dp.message_handler(lambda message: message.text == "📊 Statistika")
async def stat(message: types.Message):

    await message.answer(
        "📊 Bot ishlamoqda"
    )

# REKLAMA
@dp.message_handler(lambda message: message.text == "📢 Reklama yuborish")
async def reklama(message: types.Message):

    await message.answer(
        "📢 Reklama bo'limi"
    )

# MAJBURIY OBUNA
@dp.message_handler(lambda message: message.text == "🔐 Majburiy obuna")
async def obuna(message: types.Message):

    await message.answer(
        "🔐 Kanal obuna tizimi"
    )

# BOT START
if __name__ == "__main__":
    print("Bot ishga tushdi")
    executor.start_polling(dp, skip_updates=True)
