#!/usr/bin/env python
# coding: utf-8

import codecs
import os
from random import randint
from time import time

import telebot
from telebot import types

from max_learn import get_thought, get_fixed_thought, get_joke_b


def get_token():
	return open('.token', 'r').read()

bot = telebot.TeleBot(get_token())
STATE = {
	'rage'			:	0,
	'is_listening'	:	False,
	'is_thought'	:	False
}
response_time = 0
NICKNAMES = {
	'макс'	:	0,
	'огуз'	:	1,
	'хох'	:	1,
	'мраз'	:	2,
	'ублюд'	:	2,
	'пидрил':	3,
	'пидор'	:	3
}


@bot.message_handler(commands=['karabas'])
def stop_command(message: types.Message):
	bot.send_message(message.from_user.id, text='Ладно, я поехал.')
	print('\t/// BOT WILL BE STOPPED ///\nMaxLavrov_bot: "Ладно, я поехал."')

	os.system('python ./max_killer.py ' + str(os.getpid()))


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
		if message.content_type == 'text':
			global STATE, response_time
			now = time()
			print(f'{message.from_user.username}: "{message.text}"')

			if response_time != 0 and now - response_time >= 600:
				print(f'\t/// NOW - {now} | PREV - {response_time} ///\n\t/// LISTENING NO MORE ///')
				STATE['is_listening'] = False
				STATE['is_thought'] = False

			msg = message.text.lower()

			if STATE['is_thought']:
				bot.send_message(message.chat.id, 'Да ты еблан похлеще меня! Я это запишу...')
				file = codecs.open('./max_mind/new.txt', 'a', encoding='utf-8')
				file.write(message.text + '\n')
				STATE['is_thought'] = False
				response_time = time()
				print('MaxLavrov_bot: "Да ты еблан похлеще меня! Я это запишу..."\n\t/// NEW THOUGHT SAVED | LISTENING FOR THOUGHTS NO MORE ///')
			elif 'кринжа' in msg:
				bot.send_message(message.chat.id, '\U0001F918')
				response_time = time()
				print('MaxLavrov_bot: "\U0001F918"')
			elif is_name(msg):
				anger = get_name_anger(msg)
				if STATE['rage'] >= 5:
					STATE['rage'] = 0
				STATE['rage'] += anger
				ans = 'Да, Шэф?' if STATE['rage'] < 5 else ['Да что блять?', 'Как же ты заебал... Что?', 'Сука, когда же я подохну блять!? Что тебе?'][randint(0, 3)]
				bot.send_message(message.chat.id, ans)
				STATE['is_listening'] = True
				response_time = time()
				print(f'MaxLavrov_bot: "{ans}"\n\t/// LISTENING FOR REQUEST | RAGE = {STATE["rage"]} ///')
			elif STATE['is_listening']:
				if 'думаешь' in msg:
					thought = ''
					if randint(0, 10) > 8:
						thought = get_fixed_thought('max_mind_fixed.txt')
					else:
						thought = get_thought()
					bot.send_audio(message.chat.id, 'https://ostonline.net/dll/2019-11/8778.mp3')
					bot.send_message(message.chat.id, thought)
					response_time = time()
					print(f'MaxLavrov_bot: {thought}\n\t/// ANSWER GIVEN ///')
				elif 'как дела' in msg:
					bot.send_message(message.chat.id, 'У нас свежей завоз. Сёмга - 850 рублей за 1кг.')
					bot.send_photo(message.chat.id, 'https://sun9-41.userapi.com/impg/BuQ1UhAIP-BbijhGI8ZmKwEw6cbd4eybm2blTw/y0K31boROSo.jpg?size=1080x676&quality=96&sign=bab6b5c9dca718f99876bcbc1c55f719&type=album');
					response_time = time()
					print('MaxLavrov_bot: "У нас свежей завоз. Сёмга - 850 рублей за 1кг."\nMaxLavrov_bot: <photo>')
				elif 'новая мысль' in msg:
					bot.send_message(message.chat.id, 'Я запомню следующую мысль!')
					STATE['is_thought'] = True
					response_time = time()
					print('MaxLavrov_bot: "Я запомню следующую мысль!"\n\t/// LISTENING FOR NEW THOUGHT ///')
				elif 'расскажи анекдот' in msg:
					joke = get_joke_b()
					bot.send_message(message.chat.id, joke)
					response_time = time()
					print(f'MaxLavrov_bot: "{joke}"\n\t/// ANSWER GIVEN ///')
				elif 'молодец' in msg:
					bot.send_message(message.chat.id, 'Стараюсь, Шэф!')
					STATE['is_listening'] = False
					response_time = 0
					print('MaxLavrov_bot: "Стараюсь, Шэф!"\n\t/// LISTENING NO MORE ///')
		elif message.content_type == 'photo':
			print(f'{message.from_user.username}: <{message.content_type}>')
			bot.send_message(message.chat.id, 'Шэф, ну не при всей кухне же!')
			response_time = time()
			print('MaxLavrov_bot: "Шэф, ну не при всей кухне же!"')

print('/// BOT IS POLLING ///\nChat log:\n')
bot.set_update_listener(message_listener)
bot.polling()
