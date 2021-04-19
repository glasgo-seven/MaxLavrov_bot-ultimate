#!/usr/bin/env python
# coding: utf-8

import codecs
import os
from random import randint
from time import time, sleep

import telebot
from telebot import types

from max_mind import max_setup, get_thought, get_fixed_thought, get_joke_b
from max_learn import save_jokes

def get_token():
	# return open('.token', 'r').read()
	return os.getenv('BOT_TOKEN')


print('\n------------------------\n/// MAX IS LEARNING ///')
max_setup()
print('/// MAX READY ///')

bot = telebot.TeleBot(get_token())
STATE = {
	'rage'			:	dict(),
	'is_listening'	:	dict(),
	'is_thought'	:	list()
}
rage_trashhold = 10
RAGE_ANS = [
	'Да что блять?',
	'Как же ты заебал... Что?',
	'Сука, когда же я подохну блять!? Что тебе?'
]
RAGE_ANS_LEN = len(RAGE_ANS)
NICKNAMES = {
	'макс'	:	0,
	'огуз'	:	1,
	'хох'	:	1,
	'мраз'	:	2,
	'ублюд'	:	2,
	'гнид'	:	3,
	'пидрил':	3,
	'пидор'	:	3,
	'уеб'	:	3
}
the_lost_song_url = 'https://ostonline.net/dll/2019-11/8778.mp3'
fish_url = 'https://sun9-41.userapi.com/impg/BuQ1UhAIP-BbijhGI8ZmKwEw6cbd4eybm2blTw/y0K31boROSo.jpg?size=1080x676&quality=96&sign=bab6b5c9dca718f99876bcbc1c55f719&type=album'
max_dead_url = 'https://ibb.co/fGJkVQ4'
lolrat_sticker = 'CAACAgIAAxkBAAECL1Fgd1gAAarkud3KyoiUMaV1PK7Ylh8AAu2DAAKezgsAAZmqKq7ZUGksHwQ'


@bot.message_handler(commands=['karabas'])
def stop_command(message: types.Message):
	msg_id = f'{message.chat.id} - {message.chat.title if message.chat.title != None else "PM"} - {message.from_user.username}'
	try:
		file = open('./max_mind/user.txt')
		bot.send_document(message.chat.id, file)
	finally:
		bot.send_message(message.chat.id, text='Ладно, я поехал.')
		print(f'[{msg_id}] MaxLavrov_bot: "Ладно, я поехал."\n\t/// BOT WILL BE STOPPED ///')
		os.system('python ./max_killer.py ' + str(os.getpid()))

@bot.message_handler(commands=['help'])
def help_command(message: types.Message):
	msg_id = f'{message.chat.id} - {message.chat.title if message.chat.title != None else "PM"} - {message.from_user.username}'
	bot.send_message(message.chat.id, text='\
Привет! Я Макс из Кухни.\n\
\U000023F9Позови меня "Макс" или "Огузок".\n\
\U000023F9Спроси: "О чём думаешь?" и я выдам тебе свою умную мысль, сгенерированную специально для тебя.\n\
\U000023F9Если хочешь послушать анекдот, напиши "Анекдот". Иногда они странные, но мне нравятся.\n\
\U000023F9Если я тебе больше не нужен, напиши "Молодец".\n\
\n\
\U0001F53BМои команды:\n\
/help - Информация об основных функциях бота.\n\
/help_full - Полная помощь по функционалу бота.\n\
/update_jokes - Обновляет список анекдотов.\n\
\n\
\U0001F505v0.4 by @glasgo_seven')
	print(f'[{msg_id}] MaxLavrov_bot: help_message\n\t/// HELP MESSAGE SENT ///')

@bot.message_handler(commands=['help_full'])
def help_full_command(message: types.Message):
	msg_id = f'{message.chat.id} - {message.chat.title if message.chat.title != None else "PM"} - {message.from_user.username}'
	bot.send_message(message.chat.id, text='\
Привет! Я Макс из Кухни.\n\
\U000023F9Позови меня словами или их производными:\n\
    * Макс\n\
    * Огузок\n\
    * Хохол\n\
    * Мразь\n\
    * Ублюдок\n\
    * Гнида\n\
    * Пидрила\n\
    * Пидор\n\
    * Уёбок\n\
\U000023F9Спроси:\n\
    * "О чём думаешь?" и я выдам тебе свою умную мысль, сгенерированную специально для тебя;\n\
    * "Как дела?" и я выдам тебе смешную картинку, описывающую моё состояние.\n\
\U000023F9[НЕДОСТУПНО] Если у тебя есть какая-либо своя мысль, достойная внимания, напиши "Новая мысль", и я её запомню. Возможно...\n\
\U000023F9Если хочешь послушать анекдот, напиши "Анекдот". Иногда они странные, но мне нравятся.\n\
\U000023F9Если я тебе больше не нужен, напиши "Молодец" или пошли меня нахуй. По настроению.\n\
\n\
\U0001F53BЕщё я слежу за некоторыми ключевыми словами:\n\
    * хах\n\
    * кринж\n\
    * запусти крысу\n\
\n\
\U0001F53BМои команды:\n\
/help - Информация об основных функциях бота.\n\
/help_full - Полная помощь по функционалу бота.\n\
/update_jokes - Обновляет список анекдотов.\n\
\n\
\U0001F505v0.4 by @glasgo_seven.\n\
Всё может сломаться и обязательно сломается. Я уверен.')
	print(f'[{msg_id}] MaxLavrov_bot: help_message\n\t/// HELP_FULL MESSAGE SENT ///')

# @bot.message_handler(commands=['get_user_thoughts'])
# def get_user_thoughts_command(message: types.Message):
# 	msg_id = f'{message.chat.id} - {message.chat.title if message.chat.title != None else "PM"} - {message.from_user.username}'
# 	try:
# 		file = open('./max_mind/user.txt')
# 		bot.send_message(message.chat.id, text='Вот что люди говорят:')
# 		bot.send_document(message.chat.id, file)
# 		print(f'[{msg_id}] MaxLavrov_bot: "Вот что люди говорят:"\n[{msg_id}] MaxLavrov_bot: <document>\n\t/// USER THOUGHTS SENT ///')
# 	except FileNotFoundError:
# 		bot.send_message(message.chat.id, text='Никто ещё ничего мне не сказал.')
# 		print(f'[{msg_id}] MaxLavrov_bot: "Никто ещё ничего мне не сказал."\n\t/// NO USER THOUGHTS FOUND ///')

@bot.message_handler(commands=['update_jokes'])
def update_jokes_command(message: types.Message):
	bot.send_message(message.chat.id, text='Надеюсь там будет анекдот про двух лордов...')
	save_jokes()
	bot.send_message(message.chat.id, text='Готово!')
	msg_id = f'{message.chat.id} - {message.chat.title if message.chat.title != None else "PM"} - {message.from_user.username}'
	print(f'[{msg_id}] MaxLavrov_bot: "Надеюсь там будет анекдот про двух лордов..."\n[{msg_id}] MaxLavrov_bot: "Готово!"\n\t/// JOKES UPDATED ///')


def is_name(name):
	for n in NICKNAMES:
		if n in name:
			return True
	return False

def get_name_anger(name):
	for n in NICKNAMES:
		if n in name:
			return NICKNAMES[n]

def message_listener(*msgs):
	for message in msgs:
		message = message[0]
		msg_id = f'{message.chat.id} - {message.chat.title if message.chat.title != None else "PM"} - {message.from_user.username}'
		if message.content_type == 'text':
			global STATE
			if message.chat.id in STATE['is_listening']:
				print(f'[{msg_id}] {message.from_user.username}: "{message.text}"')

			if message.chat.id in STATE['is_listening'] and time() - STATE['is_listening'][message.chat.id] >= 600:
				print(f'\t/// NOW - {time()} | PREV - {response_time} ///\n\t/// LISTENING NO MORE ///')
				STATE['is_listening'].clear()
				STATE['is_thought'].clear()

			msg = message.text.lower()

			if message.chat.id in STATE['is_thought']:
				bot.send_message(message.chat.id, 'Да ты еблан похлеще меня! Я это запишу...')
				file = codecs.open('./max_mind/user.txt', 'a', encoding='utf-8')
				file.write(message.text + '\n')
				STATE['is_thought'].remove(message.chat.id)
				STATE['is_listening'][message.chat.id] = time()
				print(f'[{msg_id}] MaxLavrov_bot: "Да ты еблан похлеще меня! Я это запишу..."\n\t/// NEW THOUGHT SAVED | LISTENING FOR THOUGHTS NO MORE ///')
			elif 'кринж' in msg:
				if not message.chat.id in STATE['is_listening']:
					print(f'[{msg_id}] {message.from_user.username}: "{message.text}"')
				bot.send_message(message.chat.id, '\U0001F918')
				print(f'[{msg_id}] MaxLavrov_bot: "\U0001F918"')
			elif 'хах' in msg:
				if not message.chat.id in STATE['is_listening']:
					print(f'[{msg_id}] {message.from_user.username}: "{message.text}"')
				bot.send_sticker(message.chat.id, lolrat_sticker)
				print(f'[{msg_id}] MaxLavrov_bot: <sticker>')
			elif 'запус' in msg and 'крыс' in msg:
				if not message.chat.id in STATE['is_listening']:
					print(f'[{msg_id}] {message.from_user.username}: "{message.text}"')
				for i in range(10):
					bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAECL1Fgd1gAAarkud3KyoiUMaV1PK7Ylh8AAu2DAAKezgsAAZmqKq7ZUGksHwQ')
					print(f'[{msg_id}] MaxLavrov_bot: <sticker>')
					sleep(1)
			elif is_name(msg):
				if not message.chat.id in STATE['is_listening']:
					print(f'[{msg_id}] {message.from_user.username}: "{message.text}"')
				anger = get_name_anger(msg)
				if not message.chat.id in STATE['rage'] or STATE['rage'][message.chat.id] >= rage_trashhold:
					STATE['rage'][message.chat.id] = 0
				STATE['rage'][message.chat.id] += anger
				ans = 'Да, Шэф?' if STATE['rage'][message.chat.id] < rage_trashhold else RAGE_ANS[randint(0, RAGE_ANS_LEN)]
				bot.send_message(message.chat.id, ans)
				STATE['is_listening'][message.chat.id] = time()
				print(f'[{msg_id}] MaxLavrov_bot: "{ans}"\n\t/// LISTENING FOR REQUEST | RAGE = {STATE["rage"]} ///')
			elif message.chat.id in STATE['is_listening']:
				if 'думаешь' in msg:
					thought = ''
					var = ''
					if randint(0, 10) > 8:
						thought = get_fixed_thought()
						var = 'fixed'
					else:
						thought = get_thought()
						var = 'generated'
					bot.send_audio(message.chat.id, the_lost_song_url)
					try:
						bot.send_message(message.chat.id, thought)
					except:
						thought = 'Мысль огромная как ваш хуй, Шэф! Не могу так долго говорить.'
						var = 'error - responce too long'
						bot.send_message(message.chat.id, thought)
					STATE['is_listening'][message.chat.id] = time()
					print(f'[{msg_id}] MaxLavrov_bot: {thought}\n\t/// ANSWER GIVEN : {var} ///')
				elif 'как дела' in msg:
					var = ''
					if randint(0, 10) > 8:
						bot.send_photo(message.chat.id, max_dead_url)
						var = 'max_dead_url'
					else:
						# bot.send_message(message.chat.id, 'У нас свежей завоз. Сёмга - 850 рублей за 1кг.')
						bot.send_photo(message.chat.id, fish_url);
						var = 'fish_url'
						# print(f'[{msg_id}] MaxLavrov_bot: "У нас свежей завоз. Сёмга - 850 рублей за 1кг."')
					STATE['is_listening'][message.chat.id] = time()
					print(f'[{msg_id}] MaxLavrov_bot: <photo: {var}>')
				elif 'новая мысль' in msg:
					bot.send_message(message.chat.id, 'Я запомню следующую мысль!')
					STATE['is_thought'].append(message.chat.id)
					STATE['is_listening'][message.chat.id] = time()
					print(f'[{msg_id}] MaxLavrov_bot: "Я запомню следующую мысль!"\n\t/// LISTENING FOR NEW THOUGHT ///')
				elif 'анек' in msg:
					var = ''
					if randint(0, 10) > 8:
						joke = get_joke_b('\n')
						var = 'shizo'
					else:
						joke = get_joke_b()
						var = 'b'
					try:
						bot.send_message(message.chat.id, joke)
					except:
						joke = 'Анекдот моего деда, он его 4 дня рассказывал и помер. Я не буду рисковать.'
						var = 'error - responce too long'
						bot.send_message(message.chat.id, joke)
					STATE['is_listening'][message.chat.id] = time()
					print(f'[{msg_id}] MaxLavrov_bot: "{joke}"\n\t/// JOKE GIVEN : {var} ///')
				elif 'молодец' in msg:
					bot.send_message(message.chat.id, 'Стараюсь, Шэф!')
					STATE['is_listening'].pop(message.chat.id)
					print(f'[{msg_id}] MaxLavrov_bot: "Стараюсь, Шэф!"\n\t/// LISTENING NO MORE ///')
				elif 'нахуй' in msg:
					bot.send_message(message.chat.id, 'Иду нахуй, Шэф!')
					STATE['is_listening'].pop(message.chat.id)
					print(f'[{msg_id}] MaxLavrov_bot: "Иду нахуй, Шэф!"\n\t/// LISTENING NO MORE ///')
		elif message.content_type == 'photo':
			print(f'[{msg_id}] {message.from_user.username}: <{message.content_type}>')
			bot.send_message(message.chat.id, 'Шэф, ну не при всей кухне же!')
			STATE['is_listening'][message.chat.id] = time()
			print(f'[{msg_id}] MaxLavrov_bot: "Шэф, ну не при всей кухне же!"')

print('------------------------\n/// BOT IS POLLING ///\n\nChat log:\n')
bot.set_update_listener(message_listener)
bot.polling()
