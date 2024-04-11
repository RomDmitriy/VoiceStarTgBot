from src.servers.api import add_request
from src.misc.stateManager import StatusManager, StageValue
from src.bot.voices import userFriendlyVoices

from aiogram.types import Message

# Добавление заявки
async def send_confirm_message(message: Message):
	try:
		# Блокируем пользователя
		StatusManager.setState(message.from_user.id, StageValue.IS_WORKING)

		# Оформляем заявку
		place = await add_request(message.from_user.id, message.text)

		# Уведомляем пользователя
		await message.answer(f'Прекрасно!🎉\nТвой запрос уже у нас! Теперь нужно немного подождать. Твое место в очереди: {place}')
	except AttributeError:
		# AttributeError получаем, в качестве ошибки из apiServer.generate, если не выбран голос
		await message.answer('Вы не выбрали голос.\nПожалуйста, сделайте это!', reply_markup=userFriendlyVoices)
		return
	except:
		await message.answer('Неопознанная ошибка')
		return