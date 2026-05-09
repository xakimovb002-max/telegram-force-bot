import asyncio
import requests

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

TOKEN = "8645242729:AAELpQmB6-Kydw6lz6JJN11ScRUh5tAjeoQ"

ADMIN_ID = 6726095077

CHANNEL_USERNAME = "@Analyticuz"

bot = Bot(token=TOKEN)
dp = Dispatcher()

users = set()

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="💵 Valyuta kursi")],
        [KeyboardButton(text="🌤 Ob-havo")],
        [KeyboardButton(text="📊 Statistika")]
    ],
    resize_keyboard=True
)


async def check_sub(user_id):
    try:
        member = await bot.get_chat_member(
            CHANNEL_USERNAME,
            user_id
        )

        return member.status in [
            "member",
            "administrator",
            "creator"
        ]

    except:
        return False


@dp.message(CommandStart())
async def start(message: types.Message):

    users.add(message.from_user.id)

    subscribed = await check_sub(message.from_user.id)

    if not subscribed:

        btn = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="✅ Kanalga obuna bo‘lish",
                        url=f"https://t.me/{CHANNEL_USERNAME.replace('@', '')}"
                    )
                ]
            ]
        )

        await message.answer(
            "❌ Botdan foydalanish uchun kanalga obuna bo‘ling.",
            reply_markup=btn
        )

        return

    await message.answer(
        "✅ Assalomu alaykum!\n\nBot ishga tushdi.",
        reply_markup=menu
    )


@dp.message(lambda message: message.text == "💵 Valyuta kursi")
async def currency(message: types.Message):

    try:

        data = requests.get(
            "https://cbu.uz/uz/arkhiv-kursov-valyut/json/"
        ).json()

        usd = next(
            item for item in data
            if item["Ccy"] == "USD"
        )

        rub = next(
            item for item in data
            if item["Ccy"] == "RUB"
        )

        text = (
            f"💵 USD: {usd['Rate']} so'm\n"
            f"🇷🇺 RUB: {rub['Rate']} so'm"
        )

        await message.answer(text)

    except:
        await message.answer("❌ Xatolik yuz berdi.")


@dp.message(lambda message: message.text == "🌤 Ob-havo")
async def weather(message: types.Message):

    await message.answer(
        "🌤 Toshkent ob-havosi\n\n☀️ Harorat: +28°C"
    )


@dp.message(lambda message: message.text == "📊 Statistika")
async def stats(message: types.Message):

    if message.from_user.id != ADMIN_ID:
        return

    await message.answer(
        f"👥 Foydalanuvchilar soni: {len(users)}"
    )


async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
