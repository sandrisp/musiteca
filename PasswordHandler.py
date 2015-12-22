
import hashlib

salt = {'a': 'xC5o', 'c': 'X22t', 'b': 'Phdl', 'e': 'efNF', 'd': 'Un2s', 'g': 'wXDd', 'f': 'HVEg', 'i': 'Ffx2', 'h': 'HBSX', 'k': 'HHli', 'j': '17WR', 'm': '1jrI', 'l': 'wW6L', 'o': 'd4WH', 'n': 'mtZy', 'q': 'dcXe', 'p': 'OM46', 's': 'W4w7', 'r':
'2n8Y', 'u': 'kTnZ', 't': '7cJx', 'w': 'YxCG', 'v': 'FLkW', 'y': '7jAZ', 'x': 'NI40', 'z': 'l8iQ'}

from collections import defaultdict
salt = defaultdict(lambda: "AHOY", salt)

def encode(username, password):
	return hashlib.sha224(password+salt[username[0]]).hexdigest()