import csv
import pandas as pd
columnas_usuarios = ["username","Name","email","password","punteo_cuestionario","recomendacion","otras_recomendaciones"]
def abrir_archivo(nombre_archivo):
    registros = []
    with open(nombre_archivo, "r", encoding="utf8") as archivo_csv:
        lectura_archivo = csv.DictReader(archivo_csv)
        for fila in lectura_archivo:
            registros.append(fila)
    return registros

def buscar_dato(lista, dato_buscar,dato_busqueda):
    resultado = 0
    for dato in lista:
        if dato[dato_busqueda] == (dato_buscar):
            resultado = dato
    return resultado

def guardar_archivo(nombre_archivo, lista):
    with open(nombre_archivo, "w", encoding='utf8', newline='') as archivo_csv:
        escrito = csv.DictWriter(archivo_csv, fieldnames=columnas_usuarios)
        escrito.writeheader()
        for dato in lista:
            escrito.writerow(dato)

def usuario_existe(lista_usuarios, user):
    for usuario in lista_usuarios:
        if usuario['username'] == user:
            return True
    return False

def autenticacion(lista,usuario, psw):
    for user in lista:
        if user['username'] == usuario and user['password'] == psw:
            return ["True", user]
    return ["False",{}]

def calcular_punteo(respuestas):
    resultado = 0
    for respuesta in respuestas:
        lista = respuestas[respuesta].split(",")
        resultado += float(lista[0])*float(lista[1])
    return resultado
def posicion(resultado):
    posicion = ''
    if resultado > 0 and resultado <= 5:
        posicion = 'Centro'
    elif resultado > 5 and resultado <= 15:
        posicion = 'Centroderecha'
    elif resultado > 15:
        posicion = 'Derecha'
    elif resultado < 0 and resultado >= -3:
        posicion = 'Centro'
    elif resultado < -3 and resultado >= -12:
        posicion = 'Centroizquierda'
    elif resultado <-12:
        posicion = 'Izquierda'
    return posicion

def recomendar(nombre_archivo, resultado):
    pos = posicion(resultado)
    lista_partidos = pd.read_csv(nombre_archivo)
    partidos = lista_partidos.loc[lista_partidos['posicion_politica'] == pos]
    respuesta = partidos.iloc[0:3]
    otras = partidos.iloc[3:]
    respuesta_string = list(respuesta['id_partido'])
    respuesta2 = list(otras['id_partido'])
    final = ",".join(str(e) for e in respuesta_string)
    final2 = ",".join(str(e) for e in respuesta2)
    return final,final2

def graficas(nombre_archivo):
    datos = pd.read_csv(nombre_archivo)
    valores = datos['afiliados'].tolist()
    categorias = datos['siglas'].tolist()
    return [valores,categorias]