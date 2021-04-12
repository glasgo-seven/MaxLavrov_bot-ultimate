#!/usr/bin/env python
# coding: utf-8

import codecs
import random

from max_learn import get_MC_from_file_test, calc_weights, get_word

def max_setup():
	get_MC_from_file_test("./max_mind/div.txt")
	calc_weights()

def get_thought():
	fin = codecs.open('./max_mind/max.txt', 'a', encoding='utf-8')
	thought = get_word()
	fin.write(thought + '\n')
	fin.close()
	return thought

def get_fixed_thought(filename):
	return codecs.open(filename, encoding='utf-8').readlines()[random.randint(0, 7)]

def get_joke_b():
	fin = codecs.open('./max_mind/jokes.txt', 'r', encoding='utf-8')
	anek = fin.read().split('~')
	return anek[random.randint(0, len(anek) - 1)]

def get_joke_shizo():
	fin = codecs.open('./max_mind/jokes.txt', 'r', encoding='utf-8')
	anek = fin.read().split('\n')
	return anek[random.randint(0, len(anek) - 1)]
