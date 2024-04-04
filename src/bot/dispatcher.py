from src.misc.stateManager import StageManager, StageValue
from src.servers.api import getQueueStr
from src.misc.debug import is_debug
from src.bot.voices import voices

from src.bot.handlers.send_available_voices import send_available_voices
from src.bot.handlers.send_confirm_message import send_confirm_message
from src.bot.handlers.change_voice import change_voice
from src.bot.handlers.send_wait_message import send_wait_message

from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import Dispatcher


dp = Dispatcher()

# Обработка команды /start
@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
	await send_available_voices(message)

# Обработка тестовой команды /queue
# Возвращает текущую очередь
# Работает только в DEBUG_MODE
@dp.message(Command('queue'))
async def handle_queue_command(message: Message):
	if not is_debug:
		return
	
	await message.answer(getQueueStr())

# Обработка сообщения пользователя
@dp.message()
async def handle_message(message: Message) -> None:
	# Проверяем, соответствует ли сообщение какому-либо из голосов
	is_correct_voice = message.text in voices.keys()
	if is_correct_voice:
		await change_voice(message)
		return

	# Получаем состояние пользователя
	state = StageManager.getState(message.from_user.id)
	match state:
		case StageValue.IS_READY:
			# Если пользователь свободен
			await send_confirm_message(message)
		case StageValue.IS_WORKING:
			# Если пользователь занят
			await send_wait_message(message)
		case _:
			# Если у пользователя нет статуса (написал боту, пропустив команду /start)
			await send_available_voices(message)
