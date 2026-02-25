import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = "@SkechersGOWALK"

bot = telebot.TeleBot(TOKEN)


def check_sub(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if check_sub(user_id):
        bot.send_message(message.chat.id, "✅ Xush kelibsiz!")
    else:
        markup = InlineKeyboardMarkup()
        btn1 = InlineKeyboardButton("📢 Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL[1:]}")
        btn2 = InlineKeyboardButton("🔄 Tekshirish", callback_data="check")
        markup.add(btn1)
        markup.add(btn2)

        bot.send_message(
            message.chat.id,
            "❗ Botdan foydalanish uchun kanalga obuna bo‘ling:",
            reply_markup=markup
        )


@bot.callback_query_handler(func=lambda call: call.data == "check")
def callback_check(call):
    user_id = call.from_user.id

    if check_sub(user_id):
        bot.answer_callback_query(call.id, "✅ Tasdiqlandi!")
        bot.send_message(call.message.chat.id, "🎉 Endi foydalanishingiz mumkin!")
    else:
        bot.answer_callback_query(call.id, "❌ Hali obuna bo‘lmagansiz!")


bot.infinity_polling()
