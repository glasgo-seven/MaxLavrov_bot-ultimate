#!/usr/bin/env python
# coding: utf-8

import codecs
import random
import telebot

class MC_Node():
	def __init__(self, word, nodes=None):
		self.word = word
		self.edges = 1;
		self.nodes = nodes
		self.weight = 0
	
	def print_nodes(self):
		if self.nodes:
			for key in self.nodes:
				print(f'\t"{key}" : ({self.nodes[key].edges}, {self.nodes[key].weight})')
		else:
			print(f'\t({self.edges}, {self.weight})')


MARKOV_CHAIN = dict()
FIRST_WORDS = dict()
LAST_WORDS = dict()

sEnd = ['.', '!', '?', '…']
punc = [',', ';', ':']

def add_to_dict(_dict, word, nodes=None):
	if word in _dict:
		_dict[word].edges += 1
	else:
		_dict[word] = MC_Node(word, nodes)

def print_dict(_dict):
	for key in _dict:
		print(f'"{key}" : ')
		_dict[key].print_nodes()

def strip_from_marks(line):
	for mark in sEnd + punc:
		line = line.lower().replace(mark, '')
	return line

# def get_MC_from_file(filename):
# 	global MARKOV_CHAIN, FIRST_WORDS
# 	fin = codecs.open(filename, encoding='utf-8')
# 	for line in fin:
# 		words = line.strip().split()
# 		add_to_dict(FIRST_WORDS, words[0])
# 		add_to_dict(MARKOV_CHAIN, words[0], dict())
# 		for i in range(1, len(words)):
# 			if (words[i - 1][-1] in sentence_end):
# 				add_to_dict(FIRST_WORDS, words[i])
# 			add_to_dict(MARKOV_CHAIN[words[i - 1]].nodes, words[i])
# 			add_to_dict(MARKOV_CHAIN, words[i], dict())

def get_MC_from_file_test(filename):
	global MARKOV_CHAIN, FIRST_WORDS
	fin = codecs.open(filename, encoding='utf-8')
	for line in fin:
		words = line.strip().split()
		add_to_dict(FIRST_WORDS, strip_from_marks(words[0]))
		add_to_dict(MARKOV_CHAIN, strip_from_marks(words[0]), dict())
		for i in range(1, len(words)):
			if words[i - 1][-1] in sEnd:
				add_to_dict(FIRST_WORDS, strip_from_marks(words[i]))
			add_to_dict(MARKOV_CHAIN[strip_from_marks(words[i - 1])].nodes, strip_from_marks(words[i]))
			add_to_dict(MARKOV_CHAIN, strip_from_marks(words[i]), dict())
			if words[i][-1] in sEnd:
				add_to_dict(LAST_WORDS, strip_from_marks(words[i]))

def get_all_nodes(_dict):
	s = 0
	for key in _dict:
		s += _dict[key].edges
	return s

def calc_weights():
	firsts = get_all_nodes(FIRST_WORDS)
	for key in FIRST_WORDS:
		FIRST_WORDS[key].weight = FIRST_WORDS[key].edges / firsts

	for y in MARKOV_CHAIN:
		nodes = get_all_nodes(MARKOV_CHAIN[y].nodes)
		for x in MARKOV_CHAIN[y].nodes:
			MARKOV_CHAIN[y].nodes[x].weight = round(MARKOV_CHAIN[y].nodes[x].edges / nodes, 5)

	lasts = get_all_nodes(LAST_WORDS)
	for key in LAST_WORDS:
		LAST_WORDS[key].weight = LAST_WORDS[key].edges / lasts

def get_word():
	sentence = ''
	prev = ''
	
	P = random.random()
	n = 0
	for key in FIRST_WORDS:
		if n == 0:
			n = FIRST_WORDS[key].weight
		else:
			n += FIRST_WORDS[key].weight
		if P <= n:
			prev = key
			sentence += prev.capitalize()
			break

	while True:
		P = random.random()
		n = 0
		for key in MARKOV_CHAIN[prev].nodes:
			if n == 0:
				n = MARKOV_CHAIN[prev].nodes[key].weight
			else:
				n += MARKOV_CHAIN[prev].nodes[key].weight
			if P <= n:
				prev = key
				sentence += ' ' + key
				break
		if prev in LAST_WORDS:
			P = random.random()
			if P <= LAST_WORDS[prev].weight:
				sentence += '.'
				break

	return sentence


get_MC_from_file_test("./max_mind/div.txt")
calc_weights()
# print("\n-MARKOV---------\n")
# print_dict(MARKOV_CHAIN)
# print("\n-FIRST----------\n")
# print_dict(FIRST_WORDS)
# print("\n-LAST-----------\n")
# print_dict(LAST_WORDS)

def get_thought():
	return get_word()

def get_fixed_thought(filename):
	return codecs.open(filename, encoding='utf-8').readlines()[random.randint(0, 7)]

def get_joke_b():
	import vk_api
	vk_session = vk_api.VkApi(app_id=7800681,
								token='779cd56c779cd56c779cd56cb977ebd2057779c779cd56c17c6079c50a1fb427d4e1be8');
	vk = vk_session.get_api()
	li = vk.wall.get(domain='baneksbest', count=101)
	anek = li['items'][random.randint(0, 100)]['text']
	return anek
