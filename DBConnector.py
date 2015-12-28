# -*- coding: utf-8 -*-

import MySQLdb


DB_HOST="br-cdbr-azure-south-a.cloudapp.net"
DB_USER= "b270c9370980b1"
DB_PASS="03d13dd3"
DB_DATABASE = "musiteca"



def conectarDB():

	conn = MySQLdb.connect(host=DB_HOST,
				user=DB_USER,
				passwd=DB_PASS,
				db=DB_DATABASE)

	return conn