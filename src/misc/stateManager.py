from src.servers.redis import redisServer
from src.misc.debug import is_debug


# Состояния пользователя
# IS_READY - пользователь может отправлять запросы
# IS_WORKING - пользователь ждет результат
class StageValue:
	IS_READY: str = '0'
	IS_WORKING: str = '1'

# Базовый класс менеджера состояний на Redis
class _StateManager:
	_category: str = '' # строка, которая будет прибавляться к ключу (чтобы хранить одни и те же id в одной базе)

	def __init__(self, category: str) -> None:
		self._category = category

	# Получить состояние
	def getState(self, user_id: int) -> str | None:
		return redisServer.get(str(user_id) + f'_{self._category}')
	
	# Поставить состояние
	def setState(self, user_id: int, state: str) -> None:
		if is_debug:
			print(f'[StateManager - {self._category}] Set {user_id} to {state}')
		redisServer.set(str(user_id) + f'_{self._category}', state)

# Менеджер состояний
StageManager = _StateManager('stage')
# Менеджер выбора голоса
VoiceChooseManager = _StateManager('voice')
