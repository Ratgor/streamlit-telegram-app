# ./tg_bot/py_tg_bot.py

import os
import asyncio
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

API_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN')

if not API_TOKEN:
    raise ValueError("No 'TELEGRAM_BOT_API_TOKEN' provided. Please set the environment variable.")

# Initialize the bot and dispatcher
application = ApplicationBuilder().token(API_TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hi!\nI\'m your bot!\nPowered by python-telegram-bot.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Help!')

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))

async def idle():
    """Idling function to keep the bot running."""
    while True:
        print(f"DEBIG: idling (sleep 1.5)...")
        await asyncio.sleep(1.5)

async def run_bot():
    BOT_IS_RUNNING = os.getenv('TELEGRAM_BOT_IS_RUNNING')
    if not BOT_IS_RUNNING:
        os.environ['TELEGRAM_BOT_IS_RUNNING'] = str(True)
        await application.initialize()
        await application.start()
        await application.updater.start_polling()
        #await application.updater.idle()    
        #await idle()
        os.environ['TELEGRAM_BOT_IS_RUNNING'] = ""
