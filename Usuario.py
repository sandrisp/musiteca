# -*- coding: utf-8 -*-
import MySQLdb
import DBConnector
import PasswordHandler

TABLA_NOMBRE = "usuario"
TABLA_ATRIBUTOS = ["id", "usuario", "password", "correo", "nombre", "nacimiento"]

def valid_login(usuario, password):	
	conn = DBConnector.conectarDB()
	hash_pass = PasswordHandler.encode(usuario, password)
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	sql = "SELECT id FROM usuario where usuario =%s AND password=%s"
	cursor.execute(sql, [usuario, hash_pass])
	existe = cursor.fetchall()
	cursor.close()

	if len(existe) > 0:
		usuario_id = existe[0]["id"]
		return {"valido":True, "usuario_id":usuario_id}
	return {"valido":False, "usuario_id":-1}


def valid_insert_usuario(usuario):

	import re

	usuario = usuario["usuario"]
	password = usuario["password"]
	correo = usuario["correo"]
	nombre = usuario["nombre"]
	nacimiento = usuario["nacimiento"]

	salida={}
	error={}

	patron_usuario = "^[a-zA-Z]+([-+.']\w+)*$"
	patron = re.compile(patron_usuario)
	if patron.match(usuario)==None:
		error["usuario"] = (u"Debe iniciar con una letra y le puede seguir letras, números, . o _.")
	
	if not password:
		error["password"] = (u"Debe ingresar una contraseña.")
	
	patron_correo = "^\w+([-+.']\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$"
	patron = re.compile(patron_correo)
	if patron.match(correo)==None:
		error["correo"] = (u"No es un correo válido.")

	patron_nombre = "^[a-zA-Zá-úÁ-Ú]*[a-zA-Zá-úÁ-Ú ]+$"
	patron = re.compile(patron_nombre)
	if patron.match(nombre)==None:
		error["nombre"] = (u"No es un nombre válido. Solo se permiten letras y espacios.")

	import datetime
	try:
		nac = datetime.datetime.strptime(nacimiento, '%d/%m/%Y')
		today = datetime.datetime.today()
		if not nac.date()<today.date():
			error["nacimiento"] = (u"La fecha de nacimiento no puede ser después de hoy.")
	except ValueError:
		error["nacimiento"] = (u"Formato incorrecto de fecha dd/mm/aaaa.")

	if not len(error):

		conn = DBConnector.conectarDB()
		cursor = conn.cursor()
		sql = "SELECT id FROM usuario WHERE usuario =%s"
		cursor.execute(sql, [usuario])
		existe = cursor.fetchall()
		cursor.close()

		if len(existe) > 0:
			error["usuario"] = (u"El usuario ya existe.")
			salida = {"valido": False, "error": error}

		salida = {"valido": True, "error": error}
	else:
		salida = {"valido": False, "error": error}

	return salida


def insert_usuario(usuario):
	
	respuesta = valid_insert_usuario(usuario)
	
	if not respuesta["valido"]:
		return respuesta

	usuario = usuario["usuario"]
	password = usuario["password"]
	correo = usuario["correo"]
	nombre = usuario["nombre"]
	nacimiento = usuario["nacimiento"]
	conn = DBConnector.conectarDB()
	hash_pass = PasswordHandler.encode(usuario, password)
	cursor = conn.cursor()
	sql = """INSERT INTO usuario 
				(usuario, password, correo, nombre, nacimiento)
				VALUES (%s, %s, %s, %s, STR_TO_DATE(%s, %s))"""

	salida = {"valido": True, "error": ""}

	try:
		affected_count = cursor.execute(sql, [usuario, hash_pass, correo, nombre, nacimiento, '%d/%m/%Y'])
		conn.commit()
	except Exception as inst:
		salida = {"valido": False, "error": inst}
	finally:
		cursor.close()
	
	return salida

def select_usuario(usuario_id):
	conn = DBConnector.conectarDB()
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	sql = "SELECT id, usuario, password, correo, nombre, nacimiento FROM usuario where id=%s"
	cursor.execute(sql, [int(usuario_id)])
	existe = cursor.fetchall()
	cursor.close()

	if len(existe) > 0:
		usuario = existe[0]
		return usuario
	return None

def update_usuario(usuario):
	
	usuario_id = usuario["id"]
	correo = usuario["correo"]
	nombre = usuario["nombre"]
	nacimiento = usuario["nacimiento"]
	conn = DBConnector.conectarDB()
	cursor = conn.cursor()
	sql = """UPDATE usuario SET 
				correo=%s, nombre=%s, nacimiento=STR_TO_DATE(%s, %s)
				WHERE id=%s"""

	salida = {"valido": True, "error": ""}

	try:
		affected_count = cursor.execute(sql, [correo, nombre, nacimiento, '%d/%m/%Y', usuario_id])
		conn.commit()
	except Exception as inst:
		salida = {"valido": False, "error": inst}
	finally:
		cursor.close()
	
	return salida
