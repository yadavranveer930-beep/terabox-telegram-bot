import os
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ChatJoinRequestHandler, filters, ContextTypes

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
        "Aap official @telegraph bot par jaakar apna page manually bana lijiye.\n\n"
        "Phir wahan ka link mujhe bhej dijiye. Main usko Graph.org me convert karke aapke Channel ke liye ek Professional Post aur Button bana dunga! 🚀"
    )

# Private Channel Join Request Auto-Approver (Corrected Handler)
async def auto_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.chat_join_request.approve()
    except Exception as e:
        print(f"Approval Error: {e}")

async def generate_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()
    
    if text.startswith("http://") or text.startswith("https://"):
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
            "✅ **Aapki Channel Post Ready Hai!** 👇\n"
            "Niche diye gaye message ko copy ya forward karke apne channel me daal lijiye.",
            parse_mode="Markdown"
        )
        
        await update.message.reply_text(post_text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await update.message.reply_text("⚠️ Kripya mujhe sirf apna banaya hua Telegraph ya Graph.org link bhejein.")

if __name__ == '__main__':
    bot_app = ApplicationBuilder().token(TOKEN).build()
    
    # Correct Handlers
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_post))
    bot_app.add_handler(ChatJoinRequestHandler(auto_approve))
    
    bot_app.run_polling()
    
