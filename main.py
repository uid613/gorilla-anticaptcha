# Anti-Captcha for Bot Gorilla
# by vk.com/uid613

# Config

gorilla_nick = "<gorilla nick>"
token = "<token>"
owner_id = int("<your vk id>")

# Code

import vk_api # Импорт библиотеки ВКонтакте

from random import randint # Импорт функции которая будет генерировать random_id в отправке сообщения
from vk_api.longpoll import VkLongPoll, VkEventType # Импорт из библиотеки ВКонтакте модуль longpool для получения событий

on = False # Вкл/выкл
chat = None # Чат где будет анти-капча
captcha_text = gorilla_nick + ", подозрительная активность! отправьте боту «капча " # Текст капчи

vk_session = vk_api.VkApi(token=token) # Авторизация

vk = vk_session.get_api()
longpoll = VkLongPoll(vk_session)

def send_message(text): # Отправка сообщения в диалог, где оно было вызвано
	vk.messages.send(
		peer_id=event.peer_id,
		random_id=randint(1, 1e+100),
		message=str(text))

def getCaptcha(text): # Функция которая будет вытаскивать капчу из сообщения
	if text.lower().find(captcha_text) == 0:
		return text[len(captcha_text):].split()[0].replace("»", "")
	else:
		return None

while True: # Получение сообщений
	try:
		for event in longpoll.listen():
			if event.type == VkEventType.MESSAGE_NEW and event.text and event.user_id == -171493284: # Обработка сообщений от Bot Gorilla
				if event.text.lower().find(captcha_text) == 0 and on and chat == event.peer_id:
					send_message("Капча {}".format(getCaptcha(event.text)))

			if event.type == VkEventType.MESSAGE_NEW and event.text and event.user_id == owner_id: # Обработка сообщений от себя
				if event.text.lower().find('копаю в ') == 0:
					try:
						on = True
						if event.text.lower().split()[2] == "лс":
							chat = -171493284
							send_message('Анти-Капча в ЛС с Bot Gorilla успешно включена.')
						else:
							chat = 2e9 + int(event.text.split()[2])
							send_message('Анти-Капча в чате #{} успешно включена.'.format(str(int(chat-2e9))))
					except:
						on = False
						chat = None
						send_message('Ошибка. Проверьте написание команды.')

				if event.text.lower().find('айди чата') == 0:
					send_message('Айди этого чата: {}'.format(str(event.chat_id)))

				if event.text.lower().find("копаю тут") == 0:
					if event.peer_id > 2e9:
						on = True
						chat = event.peer_id
						send_message('Анти-Капча в чате #{} успешно включена.'.format(str(int(chat-2e9))))
					else:
						send_message('Данная команда работает только в чатах. Если вы хотите копать в лс Bot Gorilla то напишите "копаю в лс".')

				if event.text.lower().find('не копаю') == 0:
					on = False
					chat = None
					send_message('Анти-Капча успешно отключена.')

				if event.text.lower().find('помощь') == 0 or event.text.lower().find('команды') == 0 or event.text.lower().find('help') == 0:
					send_message('Список команд отправлен в лс.')
					vk.messages.send(
						peer_id=owner_id,
						random_id=randint(1, 1e+100),
						message="Список команд:\n\n- Копаю в [(чат айди)/ЛС]: включить анти-капчу в лс/указанном чате\n- Копаю тут: включить анти-капчу в этом чате\n- Не копаю: выключить анти-капчу\n- Айди чата: получить айди чата\n\nAnti-Captcha by @uid613")
	except Exception as e:
		print("Ошибка: ".format(str(e)))
