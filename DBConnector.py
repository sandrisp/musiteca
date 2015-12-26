# -*- coding: utf-8 -*-

import MySQLdb


DB_HOST="localhost"
DB_USER= "root"
DB_PASS=""
DB_DATABASE = "musiteca"



def conectarDB():

	conn = MySQLdb.connect(host=DB_HOST,
				user=DB_USER,
				passwd=DB_PASS,
				db=DB_DATABASE)

	return conn