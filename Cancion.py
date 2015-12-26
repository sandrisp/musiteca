# -*- coding: utf-8 -*-
import MySQLdb
import DBConnector
import Usuario
import os

TABLA_NOMBRE = "cancion"
TABLA_ATRIBUTOS = ["id", "usuario_id", "titulo", "artista", "formato", "fecha_subida"]

ALLOWED_EXTENSIONS = ["mp3"]
UPLOAD_FOLDER = 'static/music'

INSERT_ATRIBUTOS = ("usuario_id" ,"titulo" ,"artista" ,"archivos")
UPDATE_ATRIBUTOS = ("cancion_id","titulo","artista")
DELETE_ATRIBUTOS = ("cancion_id")

def valida_cancion(cancion):

	import re

	salida={}
	error={}
	
	if "cancion_id" in cancion:
		cancion_id = cancion["cancion_id"]
		if not cancion_id.isdigit() or int(cancion_id)<=0:
			error["cancion_id"] = (u"Debe ser un número positivo mayor que 0.")
		#elif select_cancion_by_id(cancion_id)==None:
			#error["cancion_id"] = (u"La canción no existe.")

	if "usuario_id" in cancion:
		usuario_id = cancion["usuario_id"]
		respuesta = Usuario.valida_usuario({"usuario_id": usuario_id})
		if not respuesta["valido"]:
			error["usuario_id"] = respuesta["error"]
	
	if "titulo" in cancion:
		titulo = cancion["titulo"]
		patron_titulo = "^[a-zA-Zá-úÁ-Ú0-9 .]+$"
		patron = re.compile(patron_titulo)
		if patron.match(titulo)==None:
			error["titulo"] = (u"Solo se permiten letras y espacios.")

	if "artista" in cancion:
		artista = cancion["artista"]
		patron_artista = "^[a-zA-Zá-úÁ-Ú0-9 .]*$"
		patron = re.compile(patron_artista)
		if patron.match(artista)==None:
			error["artista"] = (u"Solo se permiten letras y espacios.")
	
	if "archivos" in cancion:
		archivos = cancion["archivos"]
		if not 'archivo' in archivos:
			error["archivo"] = (u"Debe subir un archivo.")
		else:
			archivo = archivos["archivo"]
			file_extension_array = archivo.filename.split(".")
			formato = file_extension_array[-1]
			if not formato in ALLOWED_EXTENSIONS:
				error["archivo"] = (u"El formato debe ser "+ ', '.join(ALLOWED_EXTENSIONS))

	if not len(error):
		salida = {"valido": True, "error": error}
	else:
		salida = {"valido": False, "error": error}

	return salida

def insert_cancion(cancion):
	
	if (not all (k in cancion for k in INSERT_ATRIBUTOS)) or (not all (k in INSERT_ATRIBUTOS for k in cancion)):
		respuesta = {"valido": False, "error":"Para insertar se necesita solo el usuario_id, titulo, artista y archivos"}
		return respuesta


	respuesta = valida_cancion(cancion)
	
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

	

	sql = """INSERT INTO cancion 
				(usuario_id, titulo, artista, formato)
				VALUES (%s, %s, %s, %s)"""
	try:
		affected_count = cursor.execute(sql, [int(usuario_id), titulo, artista, formato])
		conn.commit()
		directory = UPLOAD_FOLDER+"/"+str(usuario_id)
		if not os.path.exists(directory):
			os.makedirs(directory)
		archivo.save(directory+"/"+str(cursor.lastrowid)+"."+formato)
		salida = {"valido": True, "cancion": select_cancion_by_id(str(cursor.lastrowid))}
	except Exception as inst:
		salida = {"valido": False, "error": inst}
	finally:
		cursor.close()
		conn.close()
	
	return salida

def select_cancion_by_id(cancion_id):
	conn = DBConnector.conectarDB()
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	sql = "SELECT id, usuario_id, titulo, artista, formato, DATE_FORMAT(fecha_subida, %s) fecha_subida FROM cancion where id=%s"
	cursor.execute(sql, ['%Y/%m/%d %H:%i:%S', int(cancion_id)])
	existe = cursor.fetchall()
	cursor.close()
	conn.close()

	if len(existe) > 0:
		cancion = existe[0]
		return cancion
	return None

def select_cancion_by_usuario(usuario_id):
	conn = DBConnector.conectarDB()
	cursor = conn.cursor(MySQLdb.cursors.DictCursor)
	sql = "SELECT id, usuario_id, titulo, artista, formato, DATE_FORMAT(fecha_subida, %s) fecha_subida FROM cancion where usuario_id=%s"
	cursor.execute(sql, ['%Y/%m/%d %H:%i:%S', int(usuario_id)])
	existe = cursor.fetchall()
	cursor.close()
	conn.close()

	if len(existe) > 0:
		canciones = existe
		return canciones
	return None

def update_cancion(cancion):
	
	if (not all (k in cancion for k in UPDATE_ATRIBUTOS)) or (not all (k in UPDATE_ATRIBUTOS for k in cancion)):
		respuesta = {"valido": False, "error":"Para actualizar se necesita solo el cancion_id, titulo y artista"}
		return respuesta

	respuesta = valida_cancion(cancion)
	
	if not respuesta["valido"]:
		return respuesta

	cancion_id = cancion["cancion_id"];
	titulo = cancion["titulo"];
	artista = cancion["artista"];

	conn = DBConnector.conectarDB()
	cursor = conn.cursor()
	sql = """UPDATE cancion SET 
				titulo=%s, artista=%s
				WHERE id=%s"""

	salida = {"valido": False, "error": ""}

	try:
		affected_count = cursor.execute(sql, [titulo, artista, int(cancion_id)])
		conn.commit()
		salida = {"valido": True, "cancion": select_cancion_by_id(cancion_id)}
	except Exception as inst:
		salida = {"valido": False, "error": inst}
	finally:
		cursor.close()
		conn.close()
	
	return salida

	
def delete_cancion(cancion):

	if (not "cancion_id" in cancion):
		respuesta = {"valido": False, "error":"Para borrar se necesita solo el cancion_id"}
		return respuesta


	respuesta = valida_cancion(cancion)
	
	if not respuesta["valido"]:
		return respuesta

	cancion_id = cancion["cancion_id"];


	
	cancion = select_cancion_by_id(cancion_id)
	usuario_id = cancion["usuario_id"]
	formato = cancion["formato"]



	conn = DBConnector.conectarDB()
	cursor = conn.cursor()
	sql_lista_has_cancion = """DELETE FROM lista_has_cancion WHERE cancion_id=%s"""
	

	salida = {"valido": True, "error": ""}

	try:
		affected_count_lista_has_cancion = cursor.execute(sql_lista_has_cancion, [int(cancion_id)])

		conn.commit()
	except Exception as inst:
		salida = {"valido": False, "error": inst}
		
	finally:
		cursor.close()
		conn.close()
	if(salida["valido"]==False):
		return salida
	conn = DBConnector.conectarDB()
	cursor = conn.cursor()
	sql_cancion = """DELETE FROM cancion WHERE id=%s"""
	try:
		affected_count_cancion = cursor.execute(sql_cancion, [int(cancion_id)])

		conn.commit()

		salida = {"valido": True, "cancion": {"id":cancion_id}}
	except Exception as inst2:
		salida = {"valido": False, "error": inst2}
		return salida
	finally:
		cursor.close()
		conn.close()
	os.remove(UPLOAD_FOLDER+"/"+str(usuario_id)+"/"+ cancion_id+"."+formato)
	
	return salida