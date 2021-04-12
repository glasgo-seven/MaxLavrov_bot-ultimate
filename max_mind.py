#!/usr/bin/env python
# coding: utf-8

import codecs
from random import randint

from max_learn import mc_build_from_file, mc_calculate_weights, mc_get_sentence

def max_setup():
	mc_build_from_file("./max_mind/div.txt")
	mc_calculate_weights()

def get_thought():
	fin = codecs.open('./max_mind/max.txt', 'a', encoding='utf-8')
	thought = mc_get_sentence()
	fin.write(thought + '\n')
	fin.close()
	return thought

def get_fixed_thought():
	fin = codecs.open('./max_mind/fixed.txt', encoding='utf-8')
	li = fin.read().split('\n')
	thought = li[randint(0, len(li) - 1)]
	fin.close()
	return thought

def get_joke_b(sep='~'):
	fin = codecs.open('./max_mind/jokes.txt', 'r', encoding='utf-8')
	li = fin.read().split(sep)
	joke = li[randint(0, len(li) - 1)]
	fin.close()
	return joke
