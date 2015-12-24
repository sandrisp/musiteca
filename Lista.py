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

def select_lista_by_id(lista_id):
		conn = DBConnector.conectarDB()
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		sql = "SELECT id, usuario_id, nombre FROM lista where id=%s"
		cursor.execute(sql, [int(lista_id)])
		existe = cursor.fetchall()
		cursor.close()

		if len(existe) > 0:
			lista = existe[0]
			return lista
		return None

def select_lista_by_usuario(usuario_id):
		conn = DBConnector.conectarDB()
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		sql = "SELECT id, usuario_id, nombre FROM lista where usuario_id=%s"
		cursor.execute(sql, [int(usuario_id)])
		existe = cursor.fetchall()
		cursor.close()

		if len(existe) > 0:
			listas = existe
			return listas
		return None

def delete_lista(lista):
	
	DELETE_ATRIBUTOS = ("lista_id")
	if (not all (k in lista for k in DELETE_ATRIBUTOS)) or (not all (k in DELETE_ATRIBUTOS for k in lista)):
		respuesta = {"valido": False, "error":"Para borrar se necesita solo el lista_id"}
		return respuesta

	respuesta = valida_lista(lista)
	
	if not respuesta["valido"]:
		return respuesta

	lista_id = lista["lista_id"];

	conn = DBConnector.conectarDB()
	cursor = conn.cursor()
	sql_lista_has_cancion = """DELETE FROM lista_has_cancion WHERE lista_id==%s"""
	sql_lista = """DELETE FROM lista WHERE id==%s"""

	salida = {"valido": True, "error": ""}

	try:
		affected_count_lista_has_cancion = cursor.execute(sql_lista_has_cancion, [int(lista_id)])
		affected_count_lista = cursor.execute(sql_cancion, [int(lista_id)])
		conn.commit()
	except Exception as inst:
		salida = {"valido": False, "error": inst}
	finally:
		cursor.close()
	
	return salida