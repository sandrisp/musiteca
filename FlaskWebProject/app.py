# -*- coding: utf-8 -*-

from flask import (
	Flask,
	request,
	render_template,
	redirect,
	url_for,
	session,
	Response,
	jsonify)
import Usuario
import Cancion
import Lista
import ListaHasCancion
from StreamConsumingMiddleware import StreamConsumingMiddleware
import os

app = Flask(__name__)
app.wsgi_app = StreamConsumingMiddleware(app.wsgi_app)


@app.route('/static/music/<user_id>/<cancion_id>.mp3')
def streammp3(user_id, cancion_id):
    url = url_for('static', filename='music/'+user_id+"/"+cancion_id+".mp3");
    url = os.getcwd()+url
    def generate(url):
        with open(url, "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(url), mimetype="audio/mp3")



@app.route("/")
def index_musiteca():
	usuario_sesion = check_sesion()
	if not usuario_sesion:
		return redirect(url_for('login'))

	return redirect(url_for('acciones_lista'))

def check_sesion():
	if "user_id" not in session or session["user_id"]==None:
		return 0
	else:
		return session["user_id"]


@app.route("/logout")
def logout():
	if "user_id" in session:
		session["user_id"]=None
	return redirect(url_for('login'))
@app.route('/login', methods=['GET', 'POST'])
def login():
	error = None
	if request.method == 'POST':
		respuesta = Usuario.valid_login(request.form['usuario'],
										request.form['password'])

		if respuesta["valido"]:
			session["user_id"] = respuesta["usuario_id"]
			return redirect(url_for('acciones_lista'))
		else:
			error = u"Usuario o contraseña no corresponden"
			return render_template("login.html", error=error)
	else:
		return render_template("login.html", error=error)

@app.route('/usuario/', methods=['GET', 'POST'])
def singup():
	usuario_sesion = check_sesion()
	error = None
	if request.method == 'POST':
		if usuario_sesion:
			return redirect(url_for('logout'))
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

	if request.method == 'GET':
		if usuario_sesion:
			return redirect(url_for('logout'))
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

@app.route('/usuario/<usuario_id>', methods=['GET', 'PUT'])
def acciones_usuario(usuario_id):
	usuario_sesion = check_sesion()
	if not usuario_sesion:
		return redirect(url_for('login'))

	if(str(usuario_sesion)!=usuario_id):
		return redirect(url_for('logout'))

	if request.method == 'GET':
		usuario = Usuario.select_usuario(usuario_id)
		return render_template("usuario.html", usuario=usuario, usuario_sesion=usuario_sesion)
	
	if request.method == 'PUT':
		if not all (k in Usuario.UPDATE_ATRIBUTOS for k in request.form):
			return jsonify({"valido":False, "error":"No todos los atributos para el método."})
		
		usuario={}
		usuario["usuario_id"] = usuario_sesion
		usuario["nombre"] = request.form["nombre"]
		usuario["correo"] = request.form["correo"]
		usuario["nacimiento"] = request.form["nacimiento"]

		respuesta = Usuario.update_usuario(usuario)
		return jsonify(respuesta)
@app.route('/cancion/', methods=['GET', 'POST','PUT','DELETE'])
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

@app.route('/lista/', methods=['GET', 'POST','PUT','DELETE'])
def acciones_lista():
	usuario_sesion = check_sesion()
	if not usuario_sesion:
		return redirect(url_for('login'))

	error=None
	lista = {}

	if request.method == 'GET':
		listas = Lista.select_lista_by_usuario(usuario_sesion)
		return render_template("listas.html", listas=listas, usuario_sesion=usuario_sesion)

	if request.method == 'POST':
		if not all (k in Lista.INSERT_ATRIBUTOS for k in request.form):
			return jsonify({"valido":False, "error":"No todos los atributos para el método."})
	
		lista["usuario_id"] = usuario_sesion
		lista["nombre"] = request.form["nombre"]


		respuesta = Lista.insert_lista(lista)
		return jsonify(respuesta)

	if request.method == 'PUT':
		lista["lista_id"] = request.form["lista_id"]
		lista["nombre"] = request.form["nombre"]
		lista["canciones"] = request.form.getlist("canciones")
		respuesta = Lista.update_lista(lista)
		return jsonify(respuesta)

	if request.method == 'DELETE':
		if (not "lista_id" in request.form):
			return jsonify({"valido":False, "error":"No todos los atributos para el método."})
		
		lista["lista_id"] = request.form["lista_id"]

		respuesta = Lista.delete_lista(lista)
		return jsonify(respuesta)

	return jsonify({"valido":False, "error":"Método no disponible para el recurso lista."})

@app.route('/lista/<lista_id>', methods=['GET', 'POST','PUT','DELETE'])
def acciones_lista_has_cancion(lista_id):
	usuario_sesion = check_sesion()
	if not usuario_sesion:
		return redirect(url_for('login'))

	error=None
	lista = {}

	if request.method == 'GET':
		lista = Lista.select_lista_by_id(lista_id)
		canciones = ListaHasCancion.select_canciones_by_lista(lista_id)	
		return render_template("lista_canciones.html", lista=lista, canciones=canciones, usuario_sesion=usuario_sesion)

	if request.method == 'PUT':

		canciones_usuario = ListaHasCancion.select_cancion_by_usuario_select_lista(usuario_sesion, lista_id)
		return render_template("multiselect_canciones.html",canciones_usuario=canciones_usuario)

	return jsonify({"valido":False, "error":"Método no disponible para el recurso lista."})

if __name__ == "__main__":
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run(debug=False)
