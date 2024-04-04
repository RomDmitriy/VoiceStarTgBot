from src.misc.stateManager import VoiceChooseManager, StageManager, StageValue
from src.misc.debug import is_debug
from src.bot.handlers.api_bot_handler import api_worker_handler

import requests
from os import getenv
from atexit import register
import asyncio

# Ячейка очереди запросов на генерацию
class Element:
	user_id: int
	voice: str
	text: str

	def __init__(self, user_id: int, voice: str, text: str) -> None:
		self.user_id = user_id
		self.voice = voice
		self.text = text

# Класс, отвечающий за работу с очередью запросов к API нейросети
queue: list[Element] = [] # очередь запросов

# Создать запрос в очереди. Возвращает номер в очереди от 1
async def add_request(user_id: int, text: str) -> int:
	voice = VoiceChooseManager.getState(user_id)
	if not voice:
		raise AttributeError('Голос не выбран')
	
	queue.append(Element(user_id=user_id, voice=voice, text=text))
	return len(queue)

# Бесконечный воркер, который проверяет наличие заявок и обрабатывает их в случае наличия
async def work():
	if is_debug:
		print('[Worker] Started')

	while True:
		# Если очередь пустая
		if len(queue) == 0: 
			# Следующую проверку делаем с задержкой 2 секунды
			await asyncio.sleep(2)
			continue

		if is_debug:
			print('[Worker] Sending request')

		# Берем заявку
		element = queue.pop(0)

		# Отправляем запрос
		response = requests.post(getenv('AI_GENERATE_PATH'), json={
			"data": [
				element.text, 		# Input Prompt
				"\n",		 		# Line Delimiter
				"Happy",			# Emotion
				None,				# Custom Emotion
				element.voice,		# Voice
				None,				# Sample (do not change)
				3, 					# Voice Chunks
				1, 					# Candidates (do not change)
				0, 					# Seed
				1,					# Samples TODO: 16
				2,					# Iterations. Minimum: 2 TODO: 30
				0.2,				# Temperature
				"P",				# Diffusion Samples
				8,					# Pause size
				0,					# CVVP weight
				0.8,				# Top P
				1,					# Diffusion Temperature
				1,					# Length Penalty
				2,					# Repetition Penalty
				2,					# Conditioning-Free K
				["Half Precision"], # Experimental Flags
				False,				# Use Original Latents Method (AR)
				False,				# Use Original Latents Method (Diffusion)
			]
		})

		# Разблокируем пользователя
		StageManager.setState(element.user_id, StageValue.IS_READY)

		# Если произошла ошибка запроса
		if response.status_code != 200:
			await api_worker_handler(element.user_id, None, response.status_code)
			pass

			if is_debug:
				print(f'[Worker] API error code {response.status_code} - {response.reason}: {response.content}')
			continue

		# TODO: доделать
		print(response)
		data = response.json()["data"]
		print(data)
	
# Получить номер позиции в очереди. Отсчет с 1
def getPosition(user_id: int) -> int:
	iterator: int = 0
	for elem in queue:
		if elem.user_id == user_id:
			return iterator + 1
		
		iterator += 1
	
	raise IndexError('Trying to get user\'s position, when he is\'nt in queue')

# Получить содержание очереди
def getQueueStr() -> str:
	if len(queue) == 0:
		return 'Очередь пуста!'
	
	result: str = ''
	for elem in queue:
		result += f'{elem.user_id} - {elem.voice} - {elem.text}'

	return result

# Высвобождение пользователей
# Благодаря декоратору выполняется при закрытии программы
@register
def free_users():
		for elem in queue:
			StageManager.setState(elem.user_id, StageValue.IS_READY)


