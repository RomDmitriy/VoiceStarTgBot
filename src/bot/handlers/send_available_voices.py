from src.misc.stateManager import StatusManager, StageValue
from src.bot.voices import userFriendlyVoices

from aiogram.types import Message

# Стартовое сообщение. Отправляет доступные голоса
async def send_available_voices(message: Message):
	StatusManager.setState(message.from_user.id, StageValue.IS_READY)
	await message.answer(
		"Привет! Я VoiceStar🎤 - твой персональный ⭐звездный⭐ голосовой ассистент в Telegram!\nОтправь мне текст, и мы превратим его в шедевр, озвученный голосами самых знаменитых личностей. От Черчиля до Кузнецова - выбирай своего фаворита! Начнём? Напиши текст, который ты хочешь озвучить.",
		reply_markup=userFriendlyVoices
	)