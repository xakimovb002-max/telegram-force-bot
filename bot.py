from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import requests
import asyncio

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

# KANAL TEKSHIRISH
async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(CHANNEL_USERNAME, user_id)

        if member.status in ["member", "administrator", "creator"]:
            return True

        return False

    except:
        return False

# START
@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    user_id = message.from_user.id
    users.add(user_id)

    args = message.get_args()

    if args:
        ref_id = int(args)

        if ref_id != user_id:

            if ref_id not in referrals:
                referrals[ref_id] = 0

            referrals[ref_id] += 1

    subscribed = await check_sub(user_id)

    if not subscribed:

        btn = InlineKeyboardMarkup()
        btn.add(
            InlineKeyboardButton(
                "✅ Kanalga obuna bo‘lish",
                url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"
            )
        )

        await message.answer(
            "❌ Botdan foydalanish uchun kanalga obuna bo‘ling.",
            reply_markup=btn
        )

        return

    await message.answer(
        f"👋 Assalomu alaykum\n\n🆔 Sizning ID: {user_id}\n\nBotga xush kelibsiz.",
        reply_markup=menu
    )

# REFERRAL
@dp.message_handler(lambda message: message.text == "👥 Referral sistema")
async def referral_system(message: types.Message):

    user_id = message.from_user.id

    link = f"https://t.me/{(await bot.get_me()).username}?start={user_id}"

    count = referrals.get(user_id, 0)

    await message.answer(
        f"👥 Sizning referallaringiz: {count}\n\n🔗 Havola:\n{link}"
    )

# STATISTIKA
@dp.message_handler(lambda message: message.text == "📊 Statistika")
async def stat(message: types.Message):

    await message.answer(
        f"📊 Bot foydalanuvchilari: {len(users)} ta"
    )

# OB-HAVO
@dp.message_handler(lambda message: message.text == "🌦 Ob-havo")
async def weather(message: types.Message):

    await message.answer(
        "🌦 Hozircha ob-havo funksiyasi test rejimida."
    )

# VALYUTA
@dp.message_handler(lambda message: message.text == "💵 Valyuta kursi")
async def valyuta(message: types.Message):

    try:

        data = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()

        usd = data[0]["Rate"]
        rub = data[1]["Rate"]

        await message.answer(
            f"💵 Dollar: {usd} so‘m\n🇷🇺 Rubl: {rub} so‘m"
        )

    except:

        await message.answer(
            "❌ Valyuta serverida xatolik."
        )

# MAJBURIY OBUNA
@dp.message_handler(lambda message: message.text == "🔐 Majburiy obuna")
async def majburiy(message: types.Message):

    await message.answer(
        f"🔐 Kanal: {CHANNEL_USERNAME}"
    )

# REKLAMA BOSHLASH
@dp.message_handler(lambda message: message.text == "📢 Reklama yuborish")
async def reklama_start(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        "📢 Reklama matnini yuboring."
    )

# REKLAMA YUBORISH
@dp.message_handler()
async def send_reklama(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    if message.text.startswith("/"):
        return

    buttons = [
        "👥 Referral sistema",
        "📊 Statistika",
        "🌦 Ob-havo",
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

    print("Bot ishga tushdi")

    executor.start_polling(dp, skip_updates=True)
