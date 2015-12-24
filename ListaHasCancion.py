# -*- coding: utf-8 -*-
import MySQLdb
import DBConnector

TABLA_NOMBRE = "lista_has_cancion"
TABLA_ATRIBUTOS = ["lista_id", "cancion_id", "orden"]

ALLOWED_EXTENSIONS = ["mp3"]
UPLOAD_FOLDER = 'static/music'

def valid_insert_lista_has_cancion(lista_has_cancion):

	import re

	lista_id = lista_has_cancion["lista_id"]
	cancion_id = lista_has_cancion["cancion_id"]

	salida={}
	error={}
	
	if not lista_id.isdigit() or int(lista_id)<=0:
		error["lista_id"] = (u"Debe ser un número positivo mayor que 0.")
	
	if not cancion_id.isdigit() or int(cancion_id)<=0:
		error["cancion_id"] = (u"Debe ser un número positivo mayor que 0.")

	if not len(error):
		salida = {"valido": True, "error": error}
	else:
		salida = {"valido": False, "error": error}

	return salida



def insert_lista_has_cancion(lista_has_cancion):
	
	respuesta = valid_insert_lista_has_cancion(lista_has_cancion)
	
	if not respuesta["valido"]:
		return respuesta

	lista_id = lista_has_cancion["lista_id"]
	cancion_id = lista_has_cancion["cancion_id"]

	conn = DBConnector.conectarDB()
	cursor = conn.cursor()
	sql = """INSERT INTO lista_has_cancion 
				(lista_id, cancion_id)
				VALUES (%s, %s)"""

	salida = {"valido": True, "error": ""}

	try:
		affected_count = cursor.execute(sql, [int(lista_id), int(cancion_id)])
		conn.commit()

	except Exception as inst:
		salida = {"valido": False, "error": inst}
	finally:
		cursor.close()
	
	return salida

def delete_lista_has_cancion(lista_has_cancion):
	
	DELETE_ATRIBUTOS = ("lista_id", "cancion_id")
	if (not all (k in lista_has_cancion for k in DELETE_ATRIBUTOS)) or (not all (k in DELETE_ATRIBUTOS for k in lista_has_cancion)):
		respuesta = {"valido": False, "error":"Para borrar se necesita solo el lista_id y cancion_id"}
		return respuesta

	respuesta = valida_lista_has_cancion(lista_has_cancion)
	
	if not respuesta["valido"]:
		return respuesta

	lista_id = lista_has_cancion["lista_id"];
	cancion_id = lista_has_cancion["cancion_id"];

	conn = DBConnector.conectarDB()
	cursor = conn.cursor()
	sql = """DELETE FROM lista_has_cancion WHERE lista_id==%s AND cancion_id==%s"""

	salida = {"valido": True, "error": ""}

	try:
		affected_count = cursor.execute(sql, [int(lista_id), int(cancion_id)])
		conn.commit()
	except Exception as inst:
		salida = {"valido": False, "error": inst}
	finally:
		cursor.close()
	
	return salida