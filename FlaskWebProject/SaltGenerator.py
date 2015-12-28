# -*- coding: utf-8 -*-

import random

letras = "abcdefghijklmnopqrstuvwxyz"
caracteres = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
salt={}
for j in range(0,len(letras)):
	s = ""
	for i in range(0,4):
		s += random.choice(caracteres)
	salt[letras[j]]=s

print salt

from collections import defaultdict
salt = defaultdict(lambda: "AHOY", salt)




#{'a': 'xC5o', 'c': 'X22t', 'b': 'Phdl', 'e': 'efNF', 'd': 'Un2s', 'g': 'wXDd', 'f': 'HVEg', 'i': 'Ffx2', 'h': 'HBSX', 'k': 'HHli', 'j': '17WR', 'm': '1jrI', 'l': 'wW6L', 'o': 'd4WH', 'n': 'mtZy', 'q': 'dcXe', 'p': 'OM46', 's': 'W4w7', 'r':
#'2n8Y', 'u': 'kTnZ', 't': '7cJx', 'w': 'YxCG', 'v': 'FLkW', 'y': '7jAZ', 'x': 'NI40', 'z': 'l8iQ'}