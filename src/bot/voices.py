from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Словарь доступных голосов и соответсвующим им техническим названиям
voices: dict[str, str] = {
	"📣Голос Геральта📣": "geralt",
	"📣Голос Гуры📣": "gura",
	"📣Голос Мираббаса📣": "mira",
	"📣Случайный📣": "random",
}
# Массив голосов, которые может выбрать пользователь
userFriendlyVoices = ReplyKeyboardMarkup(keyboard=list(map(lambda x: [KeyboardButton(text=x)], voices)))