from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup
import asyncio
import sqlite3
import requests

TOKEN = "8645242729:AAELpQmB6-Kydw6lz6JJN11ScRUh5tAjeoQ"
ADMIN_ID = 6726095077
CHANNEL_USERNAME = "@reklamauz_ohangaron"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = sqlite3.connect("users.db")
sql = db.cursor()

sql.execute("""
CREATE TABLE IF NOT EXISTS users (
id INTEGER
)
""")
db.commit()

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


@dp.message_handler(commands=["start"])
async def start(message: types.Message):

    user_id = message.from_user.id

    sql.execute(f"SELECT id FROM users WHERE id={user_id}")
    data = sql.fetchone()

    if data is None:
        sql.execute(f"INSERT INTO users VALUES ({user_id})")
        db.commit()

    sub = await check_sub(user_id)

    if not sub:
        btn = types.InlineKeyboardMarkup()
        btn.add(
            types.InlineKeyboardButton(
                "✅ Kanalga obuna bo'lish",
                url=f"https://t.me/{CHANNEL_USERNAME.replace('@','')}"
            )
        )

        await message.answer(
            "❌ Botdan foydalanish uchun kanalga obuna bo'ling.",
            reply_markup=btn
        )
        return

    await message.answer(
        f"👋 Assalomu alaykum\n\n🆔 Sizning ID: {user_id}\n\nBotga xush kelibsiz.",
        reply_markup=menu
    )


@dp.message_handler(lambda message: message.text == "📊 Statistika")
async def stat(message: types.Message):

    sql.execute("SELECT * FROM users")
    users = sql.fetchall()

    await message.answer(
        f"📊 Bot foydalanuvchilari: {len(users)} ta"
    )


@dp.message_handler(lambda message: message.text == "💵 Valyuta kursi")
async def valyuta(message: types.Message):

    try:
        data = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/").json()

        usd = data[0]['Rate']
        rub = data[1]['Rate']

        await message.answer(
            f"💵 USD: {usd} so'm\n🇷🇺 RUB: {rub} so'm"
        )

    except:
        await message.answer("Xatolik yuz berdi.")


@dp.message_handler(lambda message: message.text == "🌦 Ob-havo")
async def obhavo(message: types.Message):

    await message.answer(
        "🌤 Hozircha oddiy ob-havo moduli ishlayapti."
    )


@dp.message_handler(lambda message: message.text == "👥 Referral sistema")
async def referal(message: types.Message):

    link = f"https://t.me/{(await bot.get_me()).username}?start={message.from_user.id}"

    await message.answer(
        f"👥 Sizning referral linkingiz:\n\n{link}"
    )


@dp.message_handler(lambda message: message.text == "🔐 Majburiy obuna")
async def kanal(message: types.Message):

    await message.answer(
        f"🔐 Kanal: {CHANNEL_USERNAME}"
    )


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

    sql.execute("SELECT * FROM users")
    users = sql.fetchall()

    count = 0

    for user in users:
        try:
            await bot.send_message(user[0], message.text)
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
