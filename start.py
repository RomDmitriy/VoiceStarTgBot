from dotenv import load_dotenv
# Подключение .env
load_dotenv()

import logging
import sys
import asyncio
from src.bot.main import start

if __name__ == "__main__":
	logging.basicConfig(level=logging.ERROR, stream=sys.stdout)
	asyncio.run(start())