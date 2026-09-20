import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Flask Web Server setup (Render port check satisfy karne ke liye)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is live and running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Background thread mein Flask start karein
threading.Thread(target=run_flask, daemon=True).start()

# Telegram Bot Token
TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Mujhe TeraBox link bhejo, main convert kar dunga.")

async def convert_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "terabox" in text.lower() or "1024terabox" in text.lower():
        await update.message.reply_text(f"Here is your link:\n{text}")
    else:
        await update.message.reply_text("Kripya valid TeraBox link bhejein.")

if __name__ == '__main__':
    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_link))
    bot_app.run_polling()
    
    
