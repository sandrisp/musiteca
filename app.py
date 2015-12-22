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



app = Flask(__name__)

@app.route("/")
def principal():
	if "user_id" not in session or session["user_id"]==None:
		return redirect(url_for('login'))
	else:
		return redirect(url_for('hello', name="Con sesion"))


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
			session["user_id"] = respuesta["user_id"]
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
		respuesta = Usuario.insert_user(user)
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
	return jsonify(Usuario.valid_insert_user(user))


if __name__ == "__main__":
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run(debug=True)

