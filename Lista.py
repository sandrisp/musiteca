# -*- coding: utf-8 -*-
import MySQLdb
import DBConnector
import Usuario

TABLA_NOMBRE = "lista"
TABLA_ATRIBUTOS = ["id", "usuario_id", "nombre"]

INSERT_ATRIBUTOS = ("usuario_id" ,"nombre")
UPDATE_ATRIBUTOS = ("lista_id","nombre")
DELETE_ATRIBUTOS = ("lista_id")

def valida_lista(lista):

	import re

	salida={}
	error={}
	
	if "lista_id" in lista:
		lista_id = lista["lista_id"]
		if not lista_id.isdigit() or int(lista_id)<=0:
			error["lista_id"] = (u"Debe ser un número positivo mayor que 0.")
		elif select_lista_by_id(lista_id)==None:
			error["lista_id"] = (u"La lista no existe.")

	if "usuario_id" in lista:
		usuario_id = lista["usuario_id"]
		respuesta = Usuario.valida_usuario({"usuario_id": usuario_id})
		if not respuesta["valido"]:
			error["usuario_id"] = respuesta["error"]

	if "nombre" in lista:
		nombre = lista["nombre"]
		patron_nombre = "^[a-zA-Zá-úÁ-Ú0-9 ]+$"
		patron = re.compile(patron_nombre)
		if patron.match(nombre)==None:
			error["nombre"] = (u"No es un nombre válido. Solo se permiten letras y espacios.")


	if not len(error):
		salida = {"valido": True, "error": error}
	else:
		salida = {"valido": False, "error": error}

	return salida



def insert_lista(lista):
	
	if (not all (k in lista for k in INSERT_ATRIBUTOS)) or (not all (k in INSERT_ATRIBUTOS for k in lista)):
		respuesta = {"valido": False, "error":"Para insertar se necesita solo el usuario_id y nombre"}
		return respuesta

	respuesta = valida_lista(lista)
	
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

		salida = {"valido": True, "lista": select_lista_by_id(str(cursor.lastrowid))}
	except Exception as inst:
		salida = {"valido": False, "error": inst}
	finally:
		cursor.close() 
		conn.close()
	
	return salida

def select_lista_by_id(lista_id):
		conn = DBConnector.conectarDB()
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		sql = "SELECT id, usuario_id, nombre FROM lista where id=%s"
		cursor.execute(sql, [int(lista_id)])
		existe = cursor.fetchall()
		cursor.close() 
		conn.close()

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
		conn.close()

		if len(existe) > 0:
			listas = existe
			return listas
		return None


def update_lista(lista):
	
	if (not all (k in lista for k in UPDATE_ATRIBUTOS)) or (not all (k in UPDATE_ATRIBUTOS for k in lista)):
		respuesta = {"valido": False, "error":"Para actualizar se necesita solo el lista_id y nombre"}
		return respuesta

	respuesta = valida_lista(lista)
	
	if not respuesta["valido"]:
		return respuesta

	lista_id = lista["lista_id"];
	nombre = lista["nombre"];

	conn = DBConnector.conectarDB()
	cursor = conn.cursor()
	sql = """UPDATE lista SET 
				nombre=%s
				WHERE id=%s"""

	salida = {"valido": True, "error": ""}

	try:
		affected_count = cursor.execute(sql, [nombre, int(lista_id)])
		conn.commit()

		salida = {"valido": True, "lista": select_lista_by_id(lista_id)}
	except Exception as inst:
		salida = {"valido": False, "error": inst}
	finally:
		cursor.close() 
		conn.close()
	
	return salida

def delete_lista(lista):
	
	if (not "lista_id" in lista):
		respuesta = {"valido": False, "error":"Para borrar se necesita solo el lista_id"}
		return respuesta

	respuesta = valida_lista(lista)
	
	if not respuesta["valido"]:
		return respuesta

	lista_id = lista["lista_id"];

	conn = DBConnector.conectarDB()
	cursor = conn.cursor()
	sql_lista_has_cancion = """DELETE FROM lista_has_cancion WHERE lista_id=%s"""
	sql_lista = """DELETE FROM lista WHERE id=%s"""

	salida = {"valido": True, "error": ""}

	try:
		affected_count_lista_has_cancion = cursor.execute(sql_lista_has_cancion, [int(lista_id)])
		affected_count_lista = cursor.execute(sql_lista, [int(lista_id)])
		conn.commit()

		salida = {"valido": True, "lista": {"id":lista_id}}

	except Exception as inst:
		salida = {"valido": False, "error": inst}
	finally:
		cursor.close() 
		conn.close()
	
	return salida