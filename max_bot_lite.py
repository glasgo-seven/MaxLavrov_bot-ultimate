#!/usr/bin/env python
# coding: utf-8

import codecs
from random import randint
from time import time

import telebot
from telebot import types

from max_learn import get_thought, get_fixed_thought, get_joke_b

bot = telebot.TeleBot(TOKEN)
STATE = {
	'rage'			:	0,
	'is_listening'	:	False,
	'is_thought'	:	False
}
response_time = 0

# @bot.message_handler(commands=['help'])
# def help_command(message: types.Message):
# 	print(f'{message.from_user.username}: "{message.text}"')
# 	bot.send_message(message.from_user.id, text='Напиши:\n"Эй, огузок!", и я начну слушать;\n"О чём думаешь?", и я скажу тебе свою фирменную цитату.')
# 	print('\t/// SENT HELP ///\nMaxLavrov_bot: help_message')


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

			if 'огузок' in msg:
				ans = 'Да, Шэф?'
				bot.send_message(message.chat.id, ans)
				STATE['is_listening'] = True
				response_time = time()
				print(f'MaxLavrov_bot: "{ans}"\n\t/// LISTENING FOR REQUEST | RAGE = {STATE["rage"]} ///')
			elif STATE['is_listening']:
				if 'думаешь' in msg:
					thought = ''
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
				elif 'молодец' in msg:
					bot.send_message(message.chat.id, 'Стараюсь, Шэф!')
					STATE['is_listening'] = False
					response_time = 0
					print('MaxLavrov_bot: "Стараюсь, Шэф!"\n\t/// LISTENING NO MORE ///')

print('/// BOT IS POLLING ///\nChat log:\n')
bot.set_update_listener(message_listener)
bot.polling()
