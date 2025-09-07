import os
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from db import init_db
from handlers import register_handlers, register_admin_handlers
from games import register_game_handlers

TOKEN = os.getenv("BOT_TOKEN") or "YOUR_TOKEN_HERE"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

init_db()
register_handlers(dp)
register_admin_handlers(dp)
register_game_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)