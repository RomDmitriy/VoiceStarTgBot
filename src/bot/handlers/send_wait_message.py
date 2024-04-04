from src.misc.stateManager import StageManager, StageValue
from src.servers.api import getPosition
from src.bot.handlers.send_confirm_message import send_confirm_message

from aiogram.types import Message

# Обработка сообщения, когда пользователь занят
async def send_wait_message(message: Message):
	try:
		await message.answer(f'Твой текст всё ещё ожидает своей очереди😔\n Твоя позиция - {getPosition(message.from_user.id)}')
	except IndexError:
		StageManager.setState(message.from_user.id, StageValue.IS_READY)
		await send_confirm_message(message)