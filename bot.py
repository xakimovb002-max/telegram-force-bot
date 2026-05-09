from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import requests

TOKEN = "8645242729:AAELpQmB6-Kydw6lz6JJN11ScRUh5tAjeoQ"

ADMIN_ID = 6726095077
CHANNEL_USERNAME = "@reklamauz_ohangaron"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

users = set()
referrals = {}

# MENU
menu = ReplyKeyboardMarkup(resize_keyboard=True)
menu.add("👥 Referral sistema", "📊 Statistika")
menu.add("🌦 Ob-havo", "💵 Valyuta kursi")
menu.add("📢 Reklama yuborish", "🔐 Majburiy obuna")


async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)
        if member.status in ["member", "administrator", "creator"]:
            return True
        return False
    except:
        return False


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    user_id = message.from_user.id

    users.add(user_id)

    args = message.get_args()

    if args:
        ref_id = int(args)
        if ref_id != user_id:
            referrals[ref_id] = referrals.get(ref_id, 0) + 1

    sub = await check_sub(user_id)

    if not sub:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Kanalga obuna bo‘lish",
                        url="https://t.me/reklamauz_ohangaron"
                    )
                ]
            ]
        )

        await message.answer(
            "❌ Botdan foydalanish uchun kanalga obuna bo‘ling.",
            reply_markup=keyboard
        )
        return

    text = f"""
👋 Assalomu alaykum

🆔 Sizning ID: {user_id}

🤖 Botga xush kelibsiz.
"""

    await message.answer(text, reply_markup=menu)


# REFERRAL
@dp.message_handler(lambda message: message.text == "👥 Referral sistema")
async def referral_system(message: types.Message):
    user_id = message.from_user.id

    link = f"https://t.me/{(await bot.get_me()).username}?start={user_id}"

    refs = referrals.get(user_id, 0)

    text = f"""
👥 Referral sistemasi

🔗 Sizning linkingiz:
{link}

👤 Taklif qilgan odamlar: {refs} ta
"""

    await message.answer(text)


# STATISTIKA
@dp.message_handler(lambda message: message.text == "📊 Statistika")
async def stat_handler(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        f"📊 Bot statistikasi\n\n👥 Foydalanuvchilar: {len(users)} ta"
    )


# VALYUTA
@dp.message_handler(lambda message: message.text == "💵 Valyuta kursi")
async def currency_handler(message: types.Message):
    try:
        data = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()

        usd = next(item for item in data if item["Ccy"] == "USD")
        rub = next(item for item in data if item["Ccy"] == "RUB")
        eur = next(item for item in data if item["Ccy"] == "EUR")

        text = f"""
💵 Valyuta kurslari

🇺🇸 USD: {usd['Rate']} so'm
🇷🇺 RUB: {rub['Rate']} so'm
🇪🇺 EUR: {eur['Rate']} so'm
"""

        await message.answer(text)

    except:
        await message.answer("❌ Xatolik yuz berdi")


# OB-HAVO
@dp.message_handler(lambda message: message.text == "🌦 Ob-havo")
async def weather_handler(message: types.Message):
    await message.answer(
        "🌦 Ob-havo funksiyasi vaqtincha ishlamayapti"
    )


# MAJBURIY OBUNA
@dp.message_handler(lambda message: message.text == "🔐 Majburiy obuna")
async def sub_handler(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        f"🔐 Kanal: {CHANNEL_USERNAME}"
    )


# REKLAMA
@dp.message_handler(lambda message: message.text == "📢 Reklama yuborish")
async def reklama_start(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    await message.answer("📢 Reklama matnini yuboring")


@dp.message_handler()
async def send_reklama(message: types.Message):
    if message.from_user.id != ADMIN_ID:
        return

    if message.text.startswith("/"):
        return

    count = 0

    for user in users:
        try:
            await bot.send_message(user, message.text)
            count += 1
        except:
            pass

    await message.answer(f"✅ Reklama {count} ta odamga yuborildi")


if __name__ == "__main__":
    print("Bot ishga tushdi")
    executor.start_polling(dp, skip_updates=True)
