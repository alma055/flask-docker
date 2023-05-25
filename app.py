from flask import Flask, render_template, make_response, g, request, session, flash, redirect, url_for
import json
from apps.manejo_archivos import *
import os
import random
import sys

app = Flask(__name__)

app.config['SECRET_KEY'] = 'super_secret_key'
app.config['SESSION_TYPE'] = 'filesystem'

app.config['lista_partidos'] = abrir_archivo("db/partidos_politicos.csv")
app.config['usuarios'] = abrir_archivo("db/users.csv")
app.config['preguntas'] = abrir_archivo("db/cuestionario.csv")

def verificar_sesion():
    # if session.get('logged_in'):
    #     if session['logged_in']:
    #         return redirect(url_for('Inicio'))
    # if session.get('logged_in') == True:
    #     return True
    # return False
        # return redirect(url_for('Inicio'))
    #print(session['usuario'])
    if 'usuario' not in session:
        return True
        # return redirect(url_for('Inicio'))
    pass

def ini_var_session(usuario):
    session['usuario'] = usuario['username']
    session['password'] = usuario['password']
    session['name'] = usuario['Name']
    session['email'] = usuario['email']
    session['punteo'] = usuario['punteo_cuestionario']
    session['recomendacion'] = usuario['recomendacion']
    session['otras'] = usuario['otras_recomendaciones']
    session['logged_in'] = True

def end_var_session():
    session.pop('usuario', None)
    session.pop('password', None)
    session.pop('name', None)
    session.pop('email', None)
    session.pop('punteo', None)
    session.pop('recomendacion', None)
    session.pop('otras', None)
    session.pop('logged_in', None)
    return redirect(url_for('Inicio'))

@app.before_request
def antes_de_abrir():
    g.lista_partidos = app.config['lista_partidos']
    g.usuarios = app.config['usuarios']
    g.preguntas = app.config['preguntas']

@app.route('/', methods=['POST', 'GET'])
def Inicio():
    if 'usuario' in session:
        return redirect(url_for('pagina_inicial'))
    if request.method == 'POST':
        usuario = request.form['username']
        psw = request.form['password']
        autenticacion_usuario = autenticacion(g.usuarios, usuario, psw)
        if autenticacion_usuario[0] == 'False':
            flash('El usuario o la contrasenia no coinciden')
            return render_template('pages-login.html')
        ini_var_session(autenticacion_usuario[1])
        return redirect(url_for('pagina_inicial'))
    return render_template('pages-login.html')

@app.route('/pages-register',methods=['POST', 'GET'])
def crear_cuenta():
    if 'usuario' in session:
        return redirect(url_for('pagina_inicial'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        if usuario_existe(g.usuarios, username):
            flash('El usuario ya existe')
            return render_template('pages-register.html')
        registro = {"username":username, "Name":name, "email":email, "password":password, "punteo_cuestionario": '', "recomendacion":'', "otras_recomendaciones":''}
        g.usuarios.append(registro)
        guardar_archivo("db/users.csv",g.usuarios)
        return render_template('pages-login.html')
    return render_template('pages-register.html')

@app.route('/index', methods=['POST','GET'])
def pagina_inicial():
    if verificar_sesion():
        return redirect(url_for('Inicio'))
    else:
        datos = graficas('db/PartidosAfiliados.csv')
        valores_json = json.dumps(datos[0])
        categorias_json = json.dumps(datos[1])
        if session['recomendacion'] != '':
            return render_template('index.html', partidos=g.lista_partidos, resultado=[int(num) for num in session['recomendacion'].split(",")], valores = valores_json, categorias = categorias_json)
        else:
            return render_template('index.html', partidos=g.lista_partidos, valores = valores_json, categorias = categorias_json)

@app.route('/banco-informacion', methods=['POST','GET'])
def banco_informacion_general():
    if verificar_sesion():
        return redirect(url_for('Inicio'))
    else:
        return render_template('banco_informacion.html',datos = random.sample(g.lista_partidos, len(g.lista_partidos)), partidos=g.lista_partidos)

@app.route('/banco-informacion/<partido>', methods=['POST','GET'])
def informacion_partido(partido):
    if verificar_sesion():
        return redirect(url_for('Inicio'))
    else:
        especifico = buscar_dato(g.lista_partidos, partido, "siglas")
        return render_template('partido-politico.html', partidos=g.lista_partidos, especifico=especifico)

@app.route('/cuestionario', methods=['POST','GET'])
def cuestionario():
    if verificar_sesion():
        return redirect(url_for('Inicio'))
    else:
        return render_template('cuestionario.html', partidos=g.lista_partidos, preguntas=g.preguntas)
@app.route('/procesar-formulario', methods=['POST'])
def procesar_formulario():
    if verificar_sesion():
        return redirect(url_for('Inicio'))
    else:
        respuestas = {}
        for pregunta in g.preguntas:
            respuesta_key = f'p{g.preguntas.index(pregunta)+1}-{g.preguntas.index(pregunta)+1}'
            respuesta = request.form.get(respuesta_key, '')
            if respuesta == '':
                flash('Por favor responda todas las preguntas...')
                return redirect(url_for('cuestionario'))
            respuestas[respuesta_key] = respuesta
        #print(respuestas)
        registro = buscar_dato(g.usuarios, session['usuario'], 'username')
        indice = g.usuarios.index(registro)
        punteo = calcular_punteo(respuestas)
        recomendacion,otras = recomendar('db/partidos_politicos.csv', punteo)
        session['recomendacion'] = recomendacion
        g.usuarios[indice] = {"username":session['usuario'], "Name":session['name'], "email":session['email'], "password":session['password'], "punteo_cuestionario": punteo, "recomendacion":recomendacion, "otras_recomendaciones":otras}
        guardar_archivo("db/users.csv",g.usuarios)
        return redirect(url_for('resultado'))

@app.route('/resultado', methods=['GET'])
def resultado():
    if verificar_sesion():
        return redirect(url_for('Inicio'))
    else:
        return render_template('resultado.html', partidos=g.lista_partidos, resultado=[int(num) for num in session['recomendacion'].split(",")])
    
@app.route('/popularidad', methods=['GET'])
def popularidad():
    if verificar_sesion():
        return redirect(url_for('Inicio'))
    else:
        datos = graficas('db/PartidosAfiliados.csv')
        valores_json = json.dumps(datos[0])
        categorias_json = json.dumps(datos[1])
        return render_template('index.html', partidos=g.lista_partidos, valores = valores_json, categorias = categorias_json)
    
@app.route('/otras-recomendacion', methods=['GET'])
def otros():
    if verificar_sesion():
        return redirect(url_for('Inicio'))
    else:
        return render_template('resultado.html', partidos=g.lista_partidos, resultado=[int(num) for num in session['otras'].split(",")])
@app.errorhandler(404)
def not_found(error):
    """Page not found."""
    return make_response(render_template("pages-error-404.html"), 404)
@app.route('/logout')
def logout():
    end_var_session()
    return redirect("/")
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port) 