# -*- coding: utf-8 -*-
import MySQLdb
import DBConnector
import Lista
import Cancion


TABLA_NOMBRE = "lista_has_cancion"
TABLA_ATRIBUTOS = ["lista_id", "cancion_id", "orden"]

ALLOWED_EXTENSIONS = ["mp3"]
UPLOAD_FOLDER = 'static/music'

def valida_lista_has_cancion(lista_has_cancion):

	import re

	lista_id = lista_has_cancion["lista_id"]
	cancion_id = lista_has_cancion["cancion_id"]

	salida={}
	error={}
	
	if "lista_id" in lista_has_cancion:
		lista_id = lista_has_cancion["lista_id"]
		respuesta = Lista.valida_lista({"lista_id": lista_id})
		if not respuesta["valido"]:
			error["lista_id"] = respuesta["error"]

	if "cancion_id" in lista_has_cancion:
		cancion_id = lista_has_cancion["cancion_id"]
		respuesta = Cancion.valida_cancion({"cancion_id": cancion_id})
		if not respuesta["valido"]:
			error["cancion_id"] = respuesta["error"]

	if "orden" in lista_has_cancion:
		orden = lista_has_cancion["orden"]
		if not orden.isdigit() or int(orden)<0:
			error["orden"] = (u"Debe ser un número positivo mayor o igual que 0.")

	if not len(error):
		salida = {"valido": True, "error": error}
	else:
		salida = {"valido": False, "error": error}

	return salida



def insert_lista_has_cancion(lista_has_cancion):
	
	INSERT_ATRIBUTOS = ("lista_id", "cancion_id")
	if (not all (k in lista_has_cancion for k in INSERT_ATRIBUTOS)) or (not all (k in INSERT_ATRIBUTOS for k in lista_has_cancion)):
		respuesta = {"valido": False, "error":"Para insertar se necesita solo el lista_id y cancion_id"}
		return respuesta

	respuesta = valida_lista_has_cancion(lista_has_cancion)
	
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