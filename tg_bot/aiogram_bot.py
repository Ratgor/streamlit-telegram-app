# ./tg_bot/aiogram_bot.py

import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware  # does not work in aiogram 3.0+
from aiogram.utils import executor

API_TOKEN = os.getenv('TELEGRAM_BOT_API_TOKEN')

if not API_TOKEN:
    raise ValueError("No 'TELEGRAM_BOT_API_TOKEN' provided. Please set the environment variable.")

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

async def on_startup(dp):
    print('Bot is starting...')

async def on_shutdown(dp):
    await bot.close()

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm your bot!\nPowered by aiogram.")

async def run_bot():
    await executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)