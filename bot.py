import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import os

TOKEN = os.getenv("TOKEN = os.getenv("BOT_TOKEN")")  # Render'da qo'shamiz
CHANNEL = "@SkechersGOWALK"  # Majburiy obuna kanalingiz

bot = telebot.TeleBot(TOKEN)


# 🔎 Obunani tekshirish funksiyasi
def check_sub(user_id):
    try:
        member = bot.get_chat_member(CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False


# 🚀 /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id

    if check_sub(user_id):
        bot.send_message(
            message.chat.id,
            "🎉 Xush kelibsiz!\n\nSiz kanalga obuna bo‘lgansiz ✅"
        )
    else:
        markup = InlineKeyboardMarkup()
        markup.add(
            InlineKeyboardButton("📢 Kanalga obuna bo‘lish", url=f"https://t.me/{CHANNEL[1:]}")
        )
        markup.add(
            InlineKeyboardButton("✅ Tekshirish", callback_data="check_sub")
        )

        bot.send_message(
            message.chat.id,
            "❗ Botdan foydalanish uchun avval kanalga obuna bo‘ling:",
            reply_markup=markup
        )


# 🔁 Tekshirish tugmasi
@bot.callback_query_handler(func=lambda call: call.data == "check_sub")
def callback(call):
    user_id = call.from_user.id

    if check_sub(user_id):
        bot.edit_message_text(
            "🎉 Rahmat! Obuna tasdiqlandi ✅\n\nEndi botdan foydalanishingiz mumkin.",
            call.message.chat.id,
            call.message.message_id
        )
    else:
        bot.answer_callback_query(
            call.id,
            "❗ Hali kanalga obuna bo‘lmagansiz!",
            show_alert=True
        )


print("Bot ishga tushdi...")
bot.infinity_polling()
