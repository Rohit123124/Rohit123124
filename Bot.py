import telebot
import requests

# 🔐 Tokens
BOT_TOKEN = "8281750953:AAHlSSoccAHs2dt3k-LLJlI_9d3o5LqIn84"
API_TOKEN = "6827064643:4RX3BtvQ"
API_URL = "https://leakosintapi.com/"

# 🤖 Bot initialization
bot = telebot.TeleBot(BOT_TOKEN)

# 📌 Welcome message on /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_msg = (
        "👋 *Welcome to LeakCheck Bot!*\n"
        "🧠 Just send me any *phone number*, *email*, or *name* —\n"
        "and I'll search leaked data from multiple dark web sources.\n\n"
        "⚠️ *Note:* This bot is for educational/research use only.\n\n"
        "🔎 Type and send your query below ⬇️"
    )
    bot.send_message(message.chat.id, welcome_msg, parse_mode="Markdown")

# 🔍 Search Handler
@bot.message_handler(func=lambda message: True)
def search_leak(message):
    query = message.text.strip()

    searching_msg = f"🔍 *Searching leak info for:* `{{query}}`\nPlease wait a moment... ⏳"
    bot.send_message(message.chat.id, searching_msg, parse_mode="Markdown")

    # 🔧 API request setup
    payload = {
        "token": API_TOKEN,
        "request": query,
        "limit": 100,
        "lang": "en",
        "type": "json"
    }

    try:
        response = requests.post(API_URL, json=payload)
        data = response.json()

        if "List" in data and data["List"]:
            reply = f"✅ *Leaked data found for:* `{{query}}`\n\n"

            for db_name, db_data in data["List"].items():
                reply += f"📁 *Database:* {{db_name}}\n"
                info = db_data.get("InfoLeak", "")
                if info:
                    reply += f"ℹ️ {{info}}\n"

                for record in db_data.get("Data", []):
                    reply += "━━━━━━━━━━━━━━━━━━━━━━\n"
                    for key, value in record.items():
                        reply += f"*{{key}}*: `{{value}}`\n"
                    reply += "\n"

            bot.send_message(message.chat.id, reply, parse_mode="Markdown")

        else:
            bot.send_message(message.chat.id, "😕 Koi leak data nahi mila for this query.", parse_mode="Markdown")

    except Exception as e:
        error_msg = f"❗️ *Error:* `{{str(e)}}`\nKuch galti ho gayi. Try again later!"
        bot.send_message(message.chat.id, error_msg, parse_mode="Markdown")

# ▶️ Start bot
print("🚀 Bot is live and running!")
bot.infinity_polling()