from os import getenv
from aiogram import Bot
from aiogram.enums import ParseMode

# Ключ к боту
TOKEN = getenv("TELEGRAM_APITOKEN")

# Инициализируем бота
bot = Bot(TOKEN, parse_mode=ParseMode.MARKDOWN)