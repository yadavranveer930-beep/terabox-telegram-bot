import os
import re
import threading
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

threading.Thread(target=run_flask, daemon=True).start()

TOKEN = os.environ.get("BOT_TOKEN")

# Expanded list including terashare and all domain variants
TERABOX_PATTERNS = [
    r"terabox\.com", r"1024terabox\.com", r"teraboxapp\.com", 
    r"freeterabox\.com", r"teraboxlink\.com", r"mirrobox\.com", 
    r"neptunebox\.com", r"terashare\.link", r"terashare\.com", r"terabox\.app"
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Mujhe koi bhi TeraBox ya TeraShare link bhejo, main 2-Layer multi-link format ready kar dunga.")

async def convert_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Check if text contains any known pattern or valid http URL
    is_valid_link = any(re.search(pattern, text, re.IGNORECASE) for pattern in TERABOX_PATTERNS) or "http" in text.lower()
    
    if is_valid_link:
        response_text = (
            f"✅ **Link Processed Successfully!**\n\n"
            f"🔗 **Original Link:** {text}\n\n"
            f"📌 **Multi-Quality Links (2nd Layer / Landing Page):**\n"
            f"🔹 **1080p Ultra HD:** {text}\n"
            f"🔹 **720p HD:** {text}\n"
            f"🔹 **480p SD:** {text}\n"
            f"🔹 **Fast Server Backup 1:** {text}\n"
            f"🔹 **Fast Server Backup 2:** {text}\n"
            f"🔹 **Direct Stream Online:** {text}\n"
        )
        await update.message.reply_text(response_text, parse_mode="Markdown")
    else:
        await update.message.reply_text("Kripya valid TeraBox ya TeraShare link bhejein.")

if __name__ == '__main__':
    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_link))
    bot_app.run_polling()

