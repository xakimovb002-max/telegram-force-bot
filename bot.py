from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

TOKEN = "8645242729:AAELpQmB6-Kydw6lz6JJN11ScRUh5tAjeoQ"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

refs = {}

CHANNEL = "@reklamauz_ohangaron"
BOT_USERNAME = "Analyticuz_bot"

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    ref = message.get_args()
    user_id = str(message.from_user.id)

    if ref and ref != user_id:
        refs[ref] = refs.get(ref, 0) + 1

    link = f"https://t.me/{BOT_USERNAME}?start={user_id}"

    count = refs.get(user_id, 0)

    await message.answer(
        f"📢 Kanalimiz:\nhttps://t.me/reklamauz_ohangaron\n\n"
        f"🔗 Sizning referal linkingiz:\n{link}\n\n"
        f"👥 Taklif qilgan odamlar: {count}"
    )

executor.start_polling(dp)
