import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
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

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 **Welcome Boss!**\n\n"
        "Apna Telegraph link yahan bhejein, main turant Graph.org post aur button bana dunga!"
    )

async def generate_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if "telegra.ph" in text or "graph.org" in text:
        landing_page = text.replace("telegra.ph", "graph.org")
        
        post_text = (
            "🔥 **NEW POST UPLOADED** 🔥\n\n"
            "📌 **PREVIEW + WATCH ONLINE**\n"
            "➖➖➖➖➖➖➖➖➖➖\n"
            "🎬 Multiple Quality Streams Available\n"
            "⚡ Fast Server Links Attached\n"
            "🔒 Safe & Restricted Content\n"
            "➖➖➖➖➖➖➖➖➖➖\n\n"
            "👇 **Click below to access all video links:**"
        )
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("🚀 WATCH / DOWNLOAD NOW 🚀", url=landing_page)]
        ])
        
        await update.message.reply_text(
            "✅ **Aapki Channel Post Ready Hai!** 👇",
            parse_mode="Markdown"
        )
        
        await update.message.reply_text(post_text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await update.message.reply_text("⚠️ Kripya sirf valid telegra.ph ya graph.org link bhejein.")

if __name__ == '__main__':
    bot_app = ApplicationBuilder().token(TOKEN).build()
    
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_post))
    
    bot_app.run_polling()
    
