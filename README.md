Имя бота - VoiceStar🎤

1) Пользователь вводит команду /start.
2) Бот присылает приветственное сообщение:

Привет! Я VoiceStar🎤 - твой персональный ⭐звездный⭐ голосовой ассистент в Telegram!
Отправь мне текст, и мы превратим его в шедевр, озвученный голосами самых знаменитых личностей. От Черчиля до Кузнецова - выбирай своего фаворита! Начнём? Напиши текст, который ты хочешь озвучить.
--

3) Пользователь отправляет текст. Telegram имеет своё ограничение на количество символов - 4096.

4) Бот присылает сообщение:

Отлично!👍
А теперь выбери голос, который озвучит твой прекрасный текст:
--
Под этим сообщением есть две кнопки:

a) Мужской

b) Женский


5) Пользователь нажимает на одну из кнопок. 
В зависимости от выбора ему ему отправляется сообщение.

Женский:

Желаешь услышать текст в женском голосе? Нет проблем! Выбери известную личность, что тебе по душе:
--
Мужской:

Желаешь услышать текст мужским голосом? За дело! Выбери известную личность, что тебе по душе:
--

Под этими сообщениями есть кнопки, каждая из которых соответствует известной личности (этот выбор будет влиять на выбранный пресет у нейронки).

6) Пользователь нажимает на одну из кнопок, которая отвечает за выбор личности.

Бот отправляет запрос на сервер нейронки. Нейронка возвращает номер в очереди (далее ${N}).

Бот отправляет сообщение:

Прекрасно!🎉
Твой запрос уже у нас! Теперь нужно немного подождать. Твоя позиция в очереди: ${N}
--

7) Бэкенд не разрывает соединение между нейронкой и ботом. Если готово, то отправляет файл пользователю.

Если пользователь написал сообщение, пока его заказ в очереди, бот ответит:

Пожалуйста, подожди!🙏
Мы делаем всё возможное, чтобы как можно скорее закончить твой заказ.😌
--
