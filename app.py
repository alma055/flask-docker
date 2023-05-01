from flask import Flask, render_template, make_response
from apps.manejo_archivos import *
import os
import random

app = Flask(__name__)
@app.route('/', methods=['POST','GET'])
def login():
    return render_template("pages-login.html")

@app.route('/pages-register',methods=['POST', 'GET'])
def crear_cuenta():
    return render_template('pages-register.html')

@app.route('/index', methods=['POST','GET'])
def pagina_inicial():
    lista_partidos = abrir_archivo("db/partidos_politicos.csv")
    return render_template('index.html', partidos=lista_partidos)

@app.route('/banco-informacion', methods=['POST','GET'])
def banco_informacion_general():
    lista_partidos = abrir_archivo("db/partidos_politicos.csv")
    return render_template('banco_informacion.html',datos = random.sample(lista_partidos, len(lista_partidos)), partidos=lista_partidos)

# @app.route('/banco-informacion-general/<partido>', methods=['POST','GET'])
# def banco_informacion_general(partido):
#     lista_partidos = abrir_archivo("db/partidos_politicos.csv")
#     return render_template('banco_informacion.html',datos = lista_partidos)

@app.route('/users-profile',methods=['POST', 'GET'])
def info_usuario():
    lista_partidos = abrir_archivo("db/partidos_politicos.csv")
    return render_template('users-profile.html', partidos=lista_partidos)

@app.route('/pages-faq',methods=['POST', 'GET'])
def pagina_faq():
    lista_partidos = abrir_archivo("db/partidos_politicos.csv")
    return render_template('pages-faq.html', partidos=lista_partidos)

@app.route('/pages-contact',methods=['POST', 'GET'])
def pagina_contactanos():
    lista_partidos = abrir_archivo("db/partidos_politicos.csv")
    return render_template('pages-contact.html', partidos=lista_partidos)

@app.errorhandler(404)
def not_found(error):
    """Page not found."""
    return make_response(render_template("pages-error-404.html"), 404)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port) 