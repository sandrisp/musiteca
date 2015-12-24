# -*- coding: utf-8 -*-
import MySQLdb
import DBConnector

TABLA_NOMBRE = "cancion"
TABLA_ATRIBUTOS = ["id", "usuario_id", "titulo", "artista", "formato", "fecha_subida"]

ALLOWED_EXTENSIONS = ["mp3"]
UPLOAD_FOLDER = 'static/music'

def valid_insert_cancion(cancion):

	import re

	usuario_id = cancion["usuario_id"]
	titulo = cancion["titulo"]
	artista = cancion["artista"]
	archivos = cancion["archivos"]

	salida={}
	error={}
	
	if not usuario_id.isdigit() or int(usuario_id)<=0:
		error["usuario_id"] = (u"Debe ser un número positivo mayor que 0.")
	
	patron_titulo = "^[a-zA-Zá-úÁ-Ú ]+$"
	patron = re.compile(patron_titulo)
	if patron.match(titulo)==None:
		error["titulo"] = (u"Solo se permiten letras y espacios.")

	patron_artista = "^[a-zA-Zá-úÁ-Ú ]*$"
	patron = re.compile(patron_artista)
	if patron.match(artista)==None:
		error["artista"] = (u"Solo se permiten letras y espacios.")
	
	if not 'archivo' in archivos:
		error["archivo"] = (u"Debe subir un archivo.")
	else:
		archivo = archivos["archivo"]
		file_extension_array = archivo.filename.split(".")
		formato = file_extension_array[-1]
		if not formato in ALLOWED_EXTENSIONS:
			error["archivo"] = (u"El formato debe ser "+ALLOWED_EXTENSIONS)

	if not len(error):
		salida = {"valido": True, "error": error}
	else:
		salida = {"valido": False, "error": error}

	return salida

def insert_cancion(cancion):
	
	respuesta = valid_insert_cancion(cancion)
	
	if not respuesta["valido"]:
		return respuesta

	usuario_id = cancion["usuario_id"]
	titulo = cancion["titulo"]
	artista = cancion["artista"]
	archivos = cancion["archivos"]

	archivo = archivos["archivo"]
	file_extension_array = archivo.filename.split(".")
	formato = file_extension_array[-1]

	conn = DBConnector.conectarDB()
	cursor = conn.cursor()

	salida = {"valido": True, "error": ""}

	sql = """INSERT INTO cancion 
				(usuario_id, titulo, artista, formato)
				VALUES (%s, %s, %s, %s)"""
	try:
		affected_count = cursor.execute(sql, [int(usuario_id), titulo, artista, formato])
		conn.commit()
		image.save(UPLOAD_FOLDER+"/"+usuario_id+"/"+str(cursor.lastrowid)+"."+formato)

	except Exception as inst:
		salida = {"valido": False, "error": inst}
	finally:
		cursor.close()
	
	return salida

	def select_cancion_by_id(cancion_id):
		conn = DBConnector.conectarDB()
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		sql = "SELECT id, usuario_id, titulo, artista, formato, fecha_subida FROM cancion where id=%s"
		cursor.execute(sql, [int(cancion_id)])
		existe = cursor.fetchall()
		cursor.close()

		if len(existe) > 0:
			cancion = existe[0]
			return cancion
		return None

	def select_cancion_by_usuario(usuario_id):
		conn = DBConnector.conectarDB()
		cursor = conn.cursor(MySQLdb.cursors.DictCursor)
		sql = "SELECT id, usuario_id, titulo, artista, formato, fecha_subida FROM cancion where usuario_id=%s"
		cursor.execute(sql, [int(usuario_id)])
		existe = cursor.fetchall()
		cursor.close()

		if len(existe) > 0:
			canciones = existe
			return canciones
		return None
	def delete_cancion(cancion):
	
		DELETE_ATRIBUTOS = ("cancion_id")
		if (not all (k in cancion for k in DELETE_ATRIBUTOS)) or (not all (k in DELETE_ATRIBUTOS for k in cancion)):
			respuesta = {"valido": False, "error":"Para borrar se necesita solo el cancion_id"}
			return respuesta

		respuesta = valida_cancion(cancion)
		
		if not respuesta["valido"]:
			return respuesta

		cancion_id = cancion["cancion_id"];

		conn = DBConnector.conectarDB()
		cursor = conn.cursor()
		sql_lista_has_cancion = """DELETE FROM lista_has_cancion WHERE cancion_id==%s"""
		sql_cancion = """DELETE FROM cancion WHERE id==%s"""

		salida = {"valido": True, "error": ""}

		try:
			affected_count_lista_has_cancion = cursor.execute(sql_lista_has_cancion, [int(cancion_id)])
			affected_count_cancion = cursor.execute(sql_cancion, [int(cancion_id)])
			conn.commit()
		except Exception as inst:
			salida = {"valido": False, "error": inst}
		finally:
			cursor.close()
		
		return salida