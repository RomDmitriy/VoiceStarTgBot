from src.bot.dispatcher import dp
from src.bot.init import bot
from src.servers.api import work

import asyncio

# Ф-ия запуска бота
async def start():
	asyncio.create_task(work())
	await asyncio.sleep(0)

	print('[Bot] Started')

	# Запускаем бота в режиме long-pulling
	await dp.start_polling(bot)
