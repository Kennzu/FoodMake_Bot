# For bots aiogram
import asyncio
from aiogram import Bot, Dispatcher

# system imports
import logging
import sys
from pathlib import Path

# path function imports
import src.migrations.migrate as migrate

#path resources
from config import TOKEN
from src.controllers import register_handlers

# Добавляем корень проекта в пути Python
sys.path.append(str(Path(__file__).parent))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher()

register_handlers(dp)

async def main():
    migrate.backup_database()
    migrate.run_migrate()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    