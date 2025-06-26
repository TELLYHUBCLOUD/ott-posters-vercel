import os
import requests
from telegram import Update, Bot
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from lib.db import get_recent_posters

# Telegram bot setup
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
bot = Bot(token=TELEGRAM_TOKEN)

def start(update: Update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Welcome to OTT Posters Bot!\n'
        'Use /posters <platform> to get recent posters.\n'
        'Platforms: netflix, prime, disney, hbo'
    )

def send_posters(update: Update, context):
    """Send posters based on platform"""
    try:
        platform = context.args[0] if context.args else 'netflix'
        posters = get_recent_posters(platform, limit=5)
        
        if not posters:
            update.message.reply_text(f"No posters found for {platform}")
            return
            
        for poster in posters:
            update.message.reply_photo(
                photo=poster['image_url'],
                caption=f"{poster['title']} - {poster['platform']}"
            )
            
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

def setup_bot():
    """Set up the Telegram bot handlers"""
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    
    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("posters", send_posters))
    
    # Start the Bot
    updater.start_polling()
    updater.idle()

def handler(event, context):
    """Vercel serverless function handler for Telegram webhook"""
    try:
        update = Update.de_json(event.get('body'), bot)
        dispatcher.process_update(update)
        return {'statusCode': 200}
    except Exception as e:
        print(f"Error in Telegram handler: {e}")
        return {'statusCode': 500}
