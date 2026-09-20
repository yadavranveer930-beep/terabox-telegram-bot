import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Dummy web server to satisfy Render Web Service
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
    server.serve_forever()

# Start HTTP server in a separate background thread
threading.Thread(target=run_web_server, daemon=True).start()

TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! Mujhe TeraBox link bhejo, main usko converted share link mein badal dunga.")

async def convert_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if "terabox" in text.lower() or "1024terabox" in text.lower():
        await update.message.reply_text(f"Here is your link:\n{text}")
    else:
        await update.message.reply_text("Kripya valid TeraBox link bhejein.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, convert_link))
    app.run_polling()
    
