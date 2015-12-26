# -*- coding: utf-8 -*-

from flask import (
	Flask,
	request,
	render_template,
	redirect,
	url_for,
	session,
	jsonify)
import Usuario
import Cancion
from StreamConsumingMiddleware import StreamConsumingMiddleware

app = Flask(__name__)
app.wsgi_app = StreamConsumingMiddleware(app.wsgi_app)

@app.route("/null")
@app.route("/null/")
def no_null():
	return ""

def check_sesion():
	if "user_id" not in session or session["user_id"]==None:
		return 0
	else:
		return session["user_id"]


@app.route("/hello/")
@app.route('/hello/<name>')
def hello(name=None):
	# return "hello World!"
	return render_template('hello.html', name=name, user_id=session["user_id"])

@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		respuesta = Usuario.valid_login(request.form['usuario'],
										request.form['password'])
		if respuesta["valido"]:
			session["user_id"] = respuesta["usuario_id"]
			return redirect(url_for('hello', name=request.form['usuario']))
		else:
			error = u"Usuario o contraseña no corresponden"
			return render_template("login.html", error=error)
	else:
		return render_template("login.html", error=error)

@app.route('/singup', methods=['GET', 'POST'])
def singup():
	error = None
	if request.method == 'POST':
		user = {"usuario": request.form['usuario'].strip(),
				"password": request.form['password'].strip(),
				"correo": request.form['correo'].strip(),
				"nombre": request.form['nombre'].strip(),
				"nacimiento": request.form['nacimiento']
			}
		respuesta = Usuario.insert_usuario(user)
		if respuesta["valido"]:
			return render_template("login.html", error=error)
		else:
			error = respuesta["error"]
			return render_template("singup.html", error=error)
	else:
		return render_template("singup.html", error=error)

@app.route('/valid_singup', methods=['POST'])
def valid_insert_user():
	user = {"usuario": request.form['usuario'].strip(),
				"password": request.form['password'].strip(),
				"correo": request.form['correo'].strip(),
				"nombre": request.form['nombre'].strip(),
				"nacimiento": request.form['nacimiento']
			}
	return jsonify(Usuario.valida_usuario(user))

@app.route('/valida/<recurso>', methods=['POST'])
def valida(recurso=None):
	if recurso=="cancion":
		cancion = request.form.copy()
		cancion["archivos"] = request.files
		return jsonify(Cancion.valida_cancion(cancion))

	if recurso=="usuario":
		usuario = request.form.copy()
		return jsonify(Usuario.valida_usuario(usuario))

	if recurso=="lista":
		lista = request.form.copy()
		return jsonify(Lista.valida_lista(lista))

	if recurso=="lista_has_cancion":
		lista_has_cancion = request.form.copy()
		return jsonify(ListaHasCancion.valida_lista_has_cancion(lista_has_cancion))

	return jsonify({"valido":False, "error":"Recurso no disponible."})

@app.route('/cancion', methods=['GET', 'POST','PUT','DELETE'])
def acciones_cancion():
	usuario_sesion = check_sesion()
	if not usuario_sesion:
		return redirect(url_for('login'))

	error=None
	cancion = {}

	if request.method == 'GET':
		canciones = Cancion.select_cancion_by_usuario(usuario_sesion)
		return render_template("canciones.html", canciones=canciones, usuario_sesion=usuario_sesion)

	if request.method == 'POST':
		if not all (k in Cancion.INSERT_ATRIBUTOS for k in request.form):
			return jsonify({"valido":False, "error":"No todos los atributos para el método."})
	
		cancion["usuario_id"] = usuario_sesion
		cancion["titulo"] = request.form["titulo"]
		cancion["artista"] = request.form["artista"]

		cancion["archivos"] = request.files


		respuesta = Cancion.insert_cancion(cancion)
		return jsonify(respuesta)

	if request.method == 'PUT':
		if not all (k in Cancion.UPDATE_ATRIBUTOS for k in request.form):
			return jsonify({"valido":False, "error":"No todos los atributos para el método."})
		

		cancion["cancion_id"] = request.form["cancion_id"]
		cancion["titulo"] = request.form["titulo"]
		cancion["artista"] = request.form["artista"]

		respuesta = Cancion.update_cancion(cancion)
		return jsonify(respuesta)

	if request.method == 'DELETE':
		if (not "cancion_id" in request.form):
			return jsonify({"valido":False, "error":"No todos los atributos para el método."})
		
		cancion["cancion_id"] = request.form["cancion_id"]

		respuesta = Cancion.delete_cancion(cancion)
		return jsonify(respuesta)

	return jsonify({"valido":False, "error":"Método no disponible para el recurso canción."})



if __name__ == "__main__":
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run(debug=True)

