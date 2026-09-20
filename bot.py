import os
import re
import threading
import requests
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

# Function to create Telegra.ph (Graph.org) Landing Page
def create_telegraph_page(title, links_list):
    content_html = ""
    for idx, link in enumerate(links_list, 1):
        content_html += f'<li><a href="{link}">▶️ Watch / Download Video Option {idx}</a></li>\n'
    
    html_content = f'''
    <h3>🎬 Exclusive Media Collection</h3>
    <p>Select your preferred video link below to stream or download:</p>
    <ul>
        {content_html}
    </ul>
    <p><i>Note: If one link doesn't open, try another mirror link above.</i></p>
    '''
    
    try:
        response = requests.post(
            "https://api.telegra.ph/createPage",
            json={
                "access_token": "d3b25feccb89e508a9114afb82aa421fe2a9712b963b387cc5ad71e596d2",
                "title": title,
                "content": [{"tag": "p", "children": [html_content]}],
                "return_content": False
            },
            timeout=10
        )
        res_data = response.json()
        if res_data.get("ok"):
            url = res_data["result"]["url"]
            return url.replace("telegra.ph", "graph.org")
    except Exception as e:
        print(f"Telegraph API Error: {e}")
        
    return links_list[0] if links_list else ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Mujhe TeraBox links bhejo, main Graph.org landing page post bana dunga.")

async def convert_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    urls = re.findall(r'(https?://[^\s]+)', text)
    
    if urls:
        landing_page = create_telegraph_page("NEW EXCLUSIVE POST", urls)
        
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
            f"✅ **Graph.org Landing Page Ready!**\n\n"
            f"📌 **Total Links Included:** {len(urls)}\n"
            f"🔗 **Generated Link:**\n{landing_page}\n\n"
            f"👇 **Niche Aapki Channel Post Ka Preview Hai:**",
            parse_mode="Markdown"
        )
        
        await update.message.reply_text(post_text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await update.message.reply_text("Kripya valid TeraBox/TeraShare link(s) bhejein.")

if __name__ == '__main__':
    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_link))
    bot_app.run_polling()
    
