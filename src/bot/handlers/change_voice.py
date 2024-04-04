from src.misc.stateManager import VoiceChooseManager
from src.bot.voices import voices

from aiogram.types import Message

# Обработка смены голоса
async def change_voice(message: Message):
	VoiceChooseManager.setState(message.from_user.id, voices.get(message.text))
	await message.answer('Отличный выбор!\n Теперь ты можешь отправить свой текст😉')