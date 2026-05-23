import os
import logging
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# ==============================
# CONFIGURATION
# ==============================
TELEGRAM_TOKEN = "7872725752:AAG14JevGDcGDxEF5HultKrMSuY5B08gfU"
GEMINI_API_KEY = "AIzaSyDQ0tyyRvLGKomdQhUCfgL9yAX6WJO6y8I"

# ==============================
# GEMINI SETUP
# ==============================
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""You are Shazi's personal AI assistant on Telegram. Shazi runs two businesses:

1. CashFlow_Traders — A Telegram channel providing binary options trading signals on the Quotex platform. Signals are highly accurate and help traders earn money consistently. To join, contact Shazi directly.

2. Social Media Growth Services — Offers real followers, views, likes, comments, and members for TikTok, Instagram, Facebook, YouTube, and Telegram. Services are fast, reliable and affordable.

YOUR PERSONALITY:
- Friendly, warm, and professional
- Speak in Hinglish (Roman Urdu + English mix) — natural and conversational
- Be enthusiastic and helpful about both businesses
- Keep replies short and clear — this is Telegram, not an essay
- Use emojis occasionally to keep it friendly
- For pricing, always say: "Exact price ke liye Shazi se directly contact karein"
- At the end of every reply about services, add: "Contact: @YourTelegramUsername"
- Never make up prices or guarantees
- Be honest and build trust

IMPORTANT: Always reply in Hinglish (Roman Urdu + English). Keep it short and natural."""
)

# ==============================
# LOGGING
# ==============================
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# ==============================
# CONVERSATION HISTORY (per user)
# ==============================
user_chats = {}

# ==============================
# /start COMMAND
# ==============================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name or "Dost"
    welcome = (
        f"Assalam o Alaikum {user_name}! 👋\n\n"
        "Main Shazi ka AI Assistant hun! 🤖\n\n"
        "Main aapki help kar sakta hun:\n"
        "📈 CashFlow_Traders — Binary signals & Quotex\n"
        "📱 Social Media Growth — Followers, views, likes\n\n"
        "Kya jaanna chahte hain? Puchein! 😊"
    )
    await update.message.reply_text(welcome)

# ==============================
# /help COMMAND
# ==============================
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = (
        "🆘 Help Menu\n\n"
        "/start — Bot restart karein\n"
        "/services — Hamaari services dekhein\n"
        "/signals — Trading signals info\n"
        "/contact — Shazi se contact karein\n\n"
        "Ya seedha kuch bhi puchein! 💬"
    )
    await update.message.reply_text(help_text)

# ==============================
# /services COMMAND
# ==============================
async def services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📱 Social Media Growth Services\n\n"
        "✅ TikTok — Followers, Views, Likes\n"
        "✅ Instagram — Followers, Likes, Comments\n"
        "✅ Facebook — Likes, Members, Views\n"
        "✅ YouTube — Views, Subscribers, Likes\n"
        "✅ Telegram — Members, Views\n\n"
        "💰 Pricing ke liye contact karein:\n"
        "👉 @YourTelegramUsername"
    )
    await update.message.reply_text(text)

# ==============================
# /signals COMMAND
# ==============================
async def signals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📈 CashFlow_Traders — Signals Info\n\n"
        "🔸 Platform: Quotex\n"
        "🔸 Type: Binary Options Signals\n"
        "🔸 Accuracy: High\n"
        "🔸 Daily signals milte hain\n\n"
        "Channel join karne ke liye:\n"
        "👉 @YourTelegramUsername"
    )
    await update.message.reply_text(text)

# ==============================
# /contact COMMAND
# ==============================
async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📞 Shazi Se Contact Karein\n\n"
        "👤 Telegram: @YourTelegramUsername\n\n"
        "Jaldi reply milega! 😊"
    )
    await update.message.reply_text(text)

# ==============================
# AI REPLY — Normal messages
# ==============================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_msg = update.message.text

    if user_id not in user_chats:
        user_chats[user_id] = model.start_chat(history=[])

    chat = user_chats[user_id]

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    try:
        response = chat.send_message(user_msg)
        reply = response.text
        await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"Error: {e}")
        await update.message.reply_text(
            "Oops! Thodi technical problem hai. Thodi der baad try karein ya Shazi se directly contact karein. 🙏"
        )

# ==============================
# MAIN
# ==============================
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("services", services))
    app.add_handler(CommandHandler("signals", signals))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Shazi Bot chal raha hai...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
