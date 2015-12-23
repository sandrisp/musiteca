# -*- coding: utf-8 -*-
import MySQLdb
import DBConnector

TABLA_NOMBRE = "lista"
TABLA_ATRIBUTOS = ["id", "usuario_id", "nombre"]

def valid_insert_lista(lista):

	import re

	usuario_id = lista["usuario_id"]
	nombre = lista["nombre"]

	salida={}
	error={}
	
	if not usuario_id.isdigit() or int(usuario_id)<=0:
		error["usuario_id"] = (u"Debe ser un número positivo mayor que 0.")
	
	patron_nombre = "^[a-zA-Zá-úÁ-Ú ]+$"
	patron = re.compile(patron_nombre)
	if patron.match(nombre)==None:
		error["nombre"] = (u"No es un nombre válido. Solo se permiten letras y espacios.")

	if not len(error):
		salida = {"valido": True, "error": error}
	else:
		salida = {"valido": False, "error": error}

	return salida



def insert_lista(lista):
	
	respuesta = valid_insert_lista(lista)
	
	if not respuesta["valido"]:
		return respuesta

	usuario_id = lista["usuario_id"]
	nombre = lista["nombre"]

	conn = DBConnector.conectarDB()
	cursor = conn.cursor()
	sql = """INSERT INTO lista 
				(usuario_id, nombre)
				VALUES (%s, %s)"""

	salida = {"valido": True, "error": ""}

	try:
		affected_count = cursor.execute(sql, [int(usuario_id), nombre])
		conn.commit()

	except Exception as inst:
		salida = {"valido": False, "error": inst}
	finally:
		cursor.close()
	
	return salida
