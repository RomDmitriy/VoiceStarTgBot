from src.bot.init import bot

from aiogram.types import BufferedInputFile

# Обработка результата работы воркера
async def api_worker_handler(user_id: int, data: tuple[str, str], error_code: int):
	if error_code == 200:
		file = BufferedInputFile(data[0], data[1])
		await bot.send_voice(user_id, file)
		await bot.send_audio(user_id, file)

	# Если запрос не дошел до API (обычно это значит, что нейронка не запущена на указанном адресе)
	if error_code == 404:
		await bot.send_message(user_id, 'Мы сейчас испытываем технические неполадки!🔧\n Попробуйте отправить запрос чуть позже')

	# Если неопознанная ошибка (обычно это значит, что кривой запрос)
	if error_code == 500:
		await bot.send_message(user_id, 'Неопознанная ошибка⚰️\n Обратитесь к разработчикам😵‍💫')
