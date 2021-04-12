#!/usr/bin/env python
# coding: utf-8

import codecs
from random import random

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

def mc_build_from_file(filename):
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

def mc_calculate_weights():
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

def mc_get_sentence():
	sentence = ''
	prev = ''
	
	P = random()
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
		P = random()
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
			P = random()
			if P <= LAST_WORDS[prev].weight:
				sentence += '.'
				break

	return sentence

def save_jokes():
	import vk_api
	vk_session = vk_api.VkApi(app_id=7800681,
								token='779cd56c779cd56c779cd56cb977ebd2057779c779cd56c17c6079c50a1fb427d4e1be8');
	vk = vk_session.get_api()
	li = vk.wall.get(domain='baneksbest', count=101)
	fin = codecs.open('./max_mind/jokes.txt', 'w', encoding='utf-8')
	for joke in li['items']:
		fin.write(joke['text'] + '~\n')
	fin.close()

# mc_build_from_file("./max_mind/div.txt")
# mc_calculate_weights()
# save_jokes()
# mc_get_sentence()
# print("\n-MARKOV---------\n")
# print_dict(MARKOV_CHAIN)
# print("\n-FIRST----------\n")
# print_dict(FIRST_WORDS)
# print("\n-LAST-----------\n")
# print_dict(LAST_WORDS)
