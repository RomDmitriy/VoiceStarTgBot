from src.misc.stateManager import VoiceChooseManager, StatusManager, StageValue
from src.misc.debug import is_debug
from src.bot.handlers.api_bot_handler import api_worker_handler
from src.bot.voices import voice_samples

from gradio_client import Client
from os import getenv
from atexit import register
import asyncio
import requests

# Клиент для нейронки
client = Client(f'{getenv("AI_GENERATE_LINK")}')

# Ячейка очереди запросов на генерацию
class Element:
	user_id: int
	voice: tuple[str, int]
	text: str

	def __init__(self, user_id: int, voice: str, text: str) -> None:
		self.user_id = user_id
		self.voice = (voice, voice_samples.get(voice))
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
		response = client.predict(
				element.text, 			# Input Prompt
				"\n",		 			# Line Delimiter
				"None",					# Emotion
				None,					# Custom Emotion
				element.voice[0],		# Voice
				None,					# Sample (do not change)
				element.voice[1],		# Voice Chunks
				1, 						# Candidates (do not change)
				3, 						# Seed
				2,						# Samples
				2,						# Iterations. Minimum: 2
				0.2,					# Temperature
				"DDIM",					# Diffusion Samples
				8,						# Pause size
				0,						# CVVP weight
				0.8,					# Top P
				1,						# Diffusion Temperature
				1,						# Length Penalty
				2,						# Repetition Penalty
				2,						# Conditioning-Free K
				["Conditioning-Free"],	# Experimental Flags
				False,					# Use Original Latents Method (AR)
				False,					# Use Original Latents Method (Diffusion)
				api_name='/generate'
		)

		# Разблокируем пользователя
		StatusManager.setState(element.user_id, StageValue.IS_READY)

		# Если произошла ошибка запроса
		if not response[0]:
			await api_worker_handler(element.user_id, None, 500)

			# if is_debug:
			# 	print(f'[Worker] API error code {response.status_code} - {response.reason}: {response.content}')
			continue

		link: str = response[0].split('gradio\\')[1]
		filename: str = link.split('\\')[1]
		link = getenv('AI_FILES_LINK') + '/gradio/' + link

		file = requests.get(link)
		
		await api_worker_handler(element.user_id, (file.content, filename), file.status_code)
	
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
			StatusManager.setState(elem.user_id, StageValue.IS_READY)


