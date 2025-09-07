import os
from aiogram import Bot, Dispatcher
from aiogram.utils import executor
from db import init_db
from handlers import register_handlers, register_admin_handlers
from games import register_game_handlers

TOKEN = os.getenv("BOT_TOKEN") or "8238937405:AAH0F5lV29L4zAYK3UQvEuCW05lTQXCzbJA"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

init_db()
register_handlers(dp)
register_admin_handlers(dp)
register_game_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
#helko
