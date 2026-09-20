import os
import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to TeraBox Link Share Bot!\n\n"
        "Mujhe koi bhi TeraBox link ya message bhejo, main use post format mein button ke sath ready kar dunga."
    )

async def convert_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    urls = re.findall(r'(https?://[^\s]+)', text)
    
    if not urls:
        await update.message.reply_text("Kripya ek valid TeraBox link bhejein.")
        return

    main_url = urls[0]
    
    keyboard = [[InlineKeyboardButton("🎬 Watch / Download Video", url=main_url)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    caption = f"✨ **Aapki Requested File Ready Hai!** ✨\n\n🔗 [Click Here to Watch]({main_url})\n\n👇 Niche button par click karke dekhein:"
    
    await update.message.reply_text(caption, parse_mode="Markdown", reply_markup=reply_markup)

if __name__ == '__main__':
    if not BOT_TOKEN:
        print("Error: BOT_TOKEN is missing!")
        exit(1)
        
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_link))
    
    print("Bot is starting...")
    app.run_polling()
  
