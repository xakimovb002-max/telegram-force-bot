from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
import requests
import asyncio

TOKEN = "8645242729:AAELpQmB6-Kydw6lz6JJN11ScRUh5tAjeoQ"

WEATHER_API = "fb5b0254527ec050c0e71ece00768863"

ADMIN_ID = 6726095077
CHANNEL_USERNAME = "@reklamauz_ohangaron"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users = set()
referrals = {}

# MENU
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add("👥 Referral sistema", "📊 Statistika")
menu.add("🌤 Ob-havo", "💵 Valyuta kursi")
menu.add("📢 Reklama yuborish", "🔐 Majburiy obuna")


# START
@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    users.add(message.from_user.id)

    await message.answer(
        f"👋 Assalomu alaykum\n\n"
        f"🆔 Sizning ID: {message.from_user.id}\n\n"
        f"✅ Menu ishladi",
        reply_markup=menu
    )


# OB-HAVO
@dp.message_handler(lambda message: message.text == "🌤 Ob-havo")
async def weather(message: types.Message):

    city = "Tashkent"

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric"

    try:
        data = requests.get(url).json()

        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]

        await message.answer(
            f"🌤 Shahar: {city}\n"
            f"🌡 Harorat: {temp}°C\n"
            f"☁️ Holat: {desc}"
        )

    except:
        await message.answer("❌ Ob-havo olinmadi")


# VALYUTA KURSI
@dp.message_handler(lambda message: message.text == "💵 Valyuta kursi")
async def kurs(message: types.Message):

    try:
        data = requests.get(
            "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        ).json()

        usd = data[0]["Rate"]
        rub = data[1]["Rate"]
        eur = data[2]["Rate"]

        await message.answer(
            f"💵 Bugungi kurslar\n\n"
            f"🇺🇸 USD: {usd} so'm\n"
            f"🇷🇺 RUB: {rub} so'm\n"
            f"🇪🇺 EUR: {eur} so'm"
        )

    except:
        await message.answer("❌ Kurs olinmadi")


# HAR KUNLIK KURS
async def daily_kurs():

    while True:

        try:

            data = requests.get(
                "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
            ).json()

            usd = data[0]["Rate"]
            rub = data[1]["Rate"]
            eur = data[2]["Rate"]

            text = (
                f"💵 Bugungi valyuta kurslari\n\n"
                f"🇺🇸 USD: {usd} so'm\n"
                f"🇷🇺 RUB: {rub} so'm\n"
                f"🇪🇺 EUR: {eur} so'm"
            )

            for user in users:

                try:
                    await bot.send_message(user, text)

                except:
                    pass

        except:
            pass

        await asyncio.sleep(86400)


# STATISTIKA
@dp.message_handler(lambda message: message.text == "📊 Statistika")
async def stat(message: types.Message):

    await message.answer(
        f"👥 Foydalanuvchilar soni: {len(users)} ta"
    )


# REFERRAL
@dp.message_handler(lambda message: message.text == "👥 Referral sistema")
async def ref(message: types.Message):

    link = f"https://t.me/{(await bot.get_me()).username}?start={message.from_user.id}"

    await message.answer(
        f"👥 Sizning referral linkingiz:\n\n{link}"
    )


# MAJBURIY OBUNA
@dp.message_handler(lambda message: message.text == "🔐 Majburiy obuna")
async def sub(message: types.Message):

    await message.answer(
        f"🔐 Kanal: {CHANNEL_USERNAME}"
    )


# REKLAMA BOSHLASH
@dp.message_handler(lambda message: message.text == "📢 Reklama yuborish")
async def reklama(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "📢 Reklama matnini yuboring"
    )


# REKLAMA YUBORISH
@dp.message_handler()
async def send_all(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    if message.text.startswith("/"):
        return

    buttons = [
        "👥 Referral sistema",
        "📊 Statistika",
        "🌤 Ob-havo",
        "💵 Valyuta kursi",
        "📢 Reklama yuborish",
        "🔐 Majburiy obuna"
    ]

    if message.text in buttons:
        return

    count = 0

    for user in users:

        try:
            await bot.send_message(user, message.text)
            count += 1

            await asyncio.sleep(0.05)

        except:
            pass

    await message.answer(
        f"✅ Reklama {count} ta odamga yuborildi."
    )


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    loop.create_task(daily_kurs())

    print("Bot ishga tushdi")

    executor.start_polling(dp, skip_updates=True)
