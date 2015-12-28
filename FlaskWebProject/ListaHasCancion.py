# -*- coding: utf-8 -*-
import MySQLdb
import DBConnector
import Lista
import Cancion


TABLA_NOMBRE = "lista_has_cancion"
TABLA_ATRIBUTOS = ["lista_id", "cancion_id", "orden"]

INSERT_ATRIBUTOS = ("lista_id", "cancion_id")
UPDATE_ATRIBUTOS = ("lista_id","cancion_id","orden")
DELETE_ATRIBUTOS = ("lista_id", "cancion_id")

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
		try:
			if int(orden)<=0:
				error["orden"] = (u"Debe ser un número positivo mayor que 0.")
		except Exception as inst:
			error["orden"] = (u"Debe ser un número positivo mayor que 0.")

	if not len(error):
		salida = {"valido": True, "error": error}
	else:
		salida = {"valido": False, "error": error}

	return salida



def insert_lista_has_cancion(lista_has_cancion):
	
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
		salida = {"valido": True, "lista": select_canciones_by_lista(lista_id)}
	except Exception as inst:
		salida = {"valido": False, "error": inst}
	finally:
		cursor.close()
		conn.close()
	return salida

def select_canciones_by_lista(lista_id):
	conn = DBConnector.conectarDB()
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	sql = """SELECT lhc.lista_id, lhc.orden, ca.id, ca.usuario_id, ca.titulo, ca.artista, ca.formato, ca.fecha_subida
				FROM lista_has_cancion lhc 
				INNER JOIN cancion ca ON lhc.cancion_id=ca.id 
				WHERE lhc.lista_id=%s
				ORDER BY lhc.orden"""
	cursor.execute(sql, [int(lista_id)])
	existe = cursor.fetchall()
	cursor.close() 
	conn.close()

	if len(existe) > 0:
		listas = existe
		return listas
	return None
def select_cancion_by_usuario_select_lista(usuario_id, lista_id):
	conn = DBConnector.conectarDB()
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	sql = """SELECT *, IF(lhc.lista_id=%s, 'selected', '') selected 
				FROM cancion ca 
				LEFT JOIN lista_has_cancion lhc ON ca.id=lhc.cancion_id 
				WHERE ca.usuario_id=%s"""
	cursor.execute(sql, [int(lista_id), int(usuario_id)])
	existe = cursor.fetchall()
	cursor.close() 
	conn.close()

	if len(existe) > 0:
		listas = existe
		return listas
	return None

def update_lista_has_cancion(lista_has_cancion):
	
	if (not all (k in lista_has_cancion for k in UPDATE_ATRIBUTOS)) or (not all (k in UPDATE_ATRIBUTOS for k in lista_has_cancion)):
		respuesta = {"valido": False, "error":"Para actualizar se necesita solo el lista_id, cancion_id y orden"}
		return respuesta

	respuesta = valida_lista_has_cancion(lista_has_cancion)
	
	if not respuesta["valido"]:
		return respuesta

	lista_id = lista_has_cancion["lista_id"];
	cancion_id = lista_has_cancion["cancion_id"];
	orden = lista_has_cancion["orden"];

	conn = DBConnector.conectarDB()
	cursor = conn.cursor()
	sql = """UPDATE lista_has_cancion SET 
				orden=%s
				WHERE lista_id=%s AND cancion_id=%s"""

	salida = {"valido": True, "error": ""}

	try:
		affected_count = cursor.execute(sql, [orden, int(lista_id), int(cancion_id)])
		conn.commit()

		salida = {"valido": True, "lista": select_canciones_by_lista(lista_id)}
	except Exception as inst:
		salida = {"valido": False, "error": inst}
	finally:
		cursor.close()
		conn.close()
	
	return salida



def delete_lista_has_cancion(lista_has_cancion):
	
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
	sql = """DELETE FROM lista_has_cancion WHERE lista_id=%s AND cancion_id=%s"""

	salida = {"valido": True, "error": ""}

	try:
		affected_count = cursor.execute(sql, [int(lista_id), int(cancion_id)])
		conn.commit()
		salida = {"valido": True, "lista": {"id":lista_id}}
	except Exception as inst:
		salida = {"valido": False, "error": inst}
	finally:
		cursor.close()
		conn.close()
	return salida