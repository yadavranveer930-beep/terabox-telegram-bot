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

# Function to create Telegra.ph (Graph.org) Landing Page with Images & Links
def create_telegraph_page(title, items):
    # Generating HTML list items with images and links
    content_html = ""
    for idx, item in enumerate(items, 1):
        img_tag = f'<img src="{item["image"]}"/>' if item.get("image") else ''
        content_html += f'''
        <h4>🎬 Video Option {idx}: {item.get("caption", "Exclusive Video")}</h4>
        {img_tag}
        <p><a href="{item["link"]}">▶️ Watch Online / High Quality Download Server {idx}</a></p>
        <hr/>
        '''
    
    html_content = f'''
    <h3>🔥 Exclusive Media Collection</h3>
    <p>Select your video below to stream or download:</p>
    {content_html}
    <p><i>Note: Use Chrome or Brave browser for best streaming speed.</i></p>
    '''
    
    response = requests.post(
        "https://api.telegra.ph/createPage",
        json={
            "access_token": "d3b25feccb89e508a9114afb82aa421fe2a9712b963b387cc5ad71e596d2",
            "title": title,
            "content": [{"tag": "p", "children": [html_content]}],
            "return_content": False
        }
    )
    
    res_data = response.json()
    if res_data.get("ok"):
        url = res_data["result"]["url"]
        return url.replace("telegra.ph", "graph.org")
    return items[0]["link"] if items else ""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 **Welcome!**\n\n"
        "Mujhe 1 se 5 links (aur image URLs/Photos) bhejo.\n"
        "Main layout bana kar aapko Graph.org link aur Channel Post Preview dunga."
    )

# Automatic Channel Join Request Approver
async def auto_approve(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.chat_join_request.approve()
    except Exception as e:
        print(f"Error approving user: {e}")

async def convert_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    # Extract all links
    urls = re.findall(r'(https?://[^\s]+)', text)
    
    if urls:
        items = []
        for idx, url in enumerate(urls, 1):
            items.append({
                "link": url,
                "caption": f"Quality Batch #{idx}",
                "image": "" # Auto-layout
            })
            
        landing_page = create_telegraph_page("NEW EXCLUSIVE POST", items)
        
        # Professional Telegram Channel Post Formatting
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
        
        # Send preview to YOU first
        await update.message.reply_text(
            f"✅ **Graph.org Landing Page Ready!**\n\n"
            f"🔗 **Generated Link:**\n{landing_page}\n\n"
            f"👇 **Niche Aapki Channel Post Ka Preview Hai:**",
            parse_mode="Markdown"
        )
        
        # Channel Post Preview
        await update.message.reply_text(post_text, reply_markup=keyboard, parse_mode="Markdown")
    else:
        await update.message.reply_text("Kripya valid TeraBox/TeraShare link(s) bhejein.")

if __name__ == '__main__':
    bot_app = ApplicationBuilder().token(TOKEN).build()
    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_link))
    bot_app.run_polling()
    
