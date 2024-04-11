from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

# Словарь доступных голосов и соответсвующим им техническим названиям
voices: dict[str, str] = {
	"📣Голос Геральта📣": "vsevolodutils_77",
	"📣Голос Гуры📣": "gura_15",
}

# Массив голосов, которые может выбрать пользователь
userFriendlyVoices = ReplyKeyboardMarkup(keyboard=list(map(lambda x: [KeyboardButton(text=x)], voices)))

# Словарь сэмплов
voice_samples: dict[str, int] = {
	"vsevolodutils": 77,
	"gura": 15
}